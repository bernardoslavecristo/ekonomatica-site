"""Exact one-day whole-lot planning with explicit, supplied constraints.

This does not reuse the game's crop constants or trained policy. All quantities
are supplied estimates. No forecasting, agronomic prescriptions or execution.
"""

import hashlib
import itertools
import json

RESOURCE_KEYS = ("budget_cents", "labor_minutes", "transport_capacity_kg", "buyer_capacity_kg")
LOT_KEYS = {"id", "harvestable_kg", "labor_minutes", "cost_cents", "price_cents_per_kg", "ready_to_harvest"}
MAX_LOTS = 16


def _integer(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f"{name}: informe um inteiro não negativo na unidade indicada")
    return value


def _identifier(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}: identificador vazio ou inválido")
    return value


def _resources(value, name):
    if not isinstance(value, dict) or set(value) != set(RESOURCE_KEYS):
        raise ValueError(f"{name}: informe exatamente {RESOURCE_KEYS}")
    return {k: _integer(value[k], f"{name}.{k}") for k in RESOURCE_KEYS}


def validate(payload):
    if not isinstance(payload, dict):
        raise ValueError("A entrada deve ser um objeto JSON")
    allowed = {"data_origin", "planning_date", "resources", "lots", "objective", "baseline_ids", "scenarios"}
    if set(payload) - allowed:
        raise ValueError("Campos desconhecidos na entrada")
    if payload.get("data_origin") not in {"synthetic", "user_supplied_estimates"}:
        raise ValueError("Declare data_origin: synthetic ou user_supplied_estimates")
    from datetime import date
    try:
        date.fromisoformat(payload["planning_date"])
    except (KeyError, ValueError, TypeError):
        raise ValueError("planning_date: informe a data de planejamento AAAA-MM-DD") from None
    _resources(payload.get("resources"), "resources")
    lots = payload.get("lots")
    if not isinstance(lots, list) or not 1 <= len(lots) <= MAX_LOTS:
        raise ValueError(f"Informe de 1 a {MAX_LOTS} lotes; não há promessa de escala além desse limite")
    ids = set()
    for lot in lots:
        if not isinstance(lot, dict) or set(lot) != LOT_KEYS:
            raise ValueError(f"Cada lote deve conter exatamente {sorted(LOT_KEYS)}")
        lot_id = _identifier(lot["id"], "lot.id")
        if lot_id in ids:
            raise ValueError("Identificadores de lote duplicados")
        ids.add(lot_id)
        for key in LOT_KEYS - {"id", "ready_to_harvest"}:
            _integer(lot[key], f"{lot_id}.{key}")
        if lot["harvestable_kg"] == 0:
            raise ValueError("Cada lote precisa ter quantidade positiva")
        if type(lot["ready_to_harvest"]) is not bool:
            raise ValueError("ready_to_harvest deve ser booleano confirmado pelo responsável")
    if payload.get("objective", "saleable_kg") not in {"saleable_kg", "contribution_cents"}:
        raise ValueError("objective: saleable_kg ou contribution_cents")
    if "baseline_ids" in payload:
        baseline = payload["baseline_ids"]
        if (not isinstance(baseline, list) or any(not isinstance(x, str) for x in baseline)
                or len(set(baseline)) != len(baseline) or set(baseline) - ids):
            raise ValueError("baseline_ids deve conter IDs existentes, sem duplicação")
    scenarios = payload.get("scenarios", [])
    if not isinstance(scenarios, list) or len(scenarios) > 8:
        raise ValueError("Informe no máximo oito cenários")
    scenario_names = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict) or set(scenario) != {"name", "resources"}:
            raise ValueError("Cada cenário precisa de name e resources completos")
        name = _identifier(scenario["name"], "scenario.name")
        if name == "base" or name in scenario_names:
            raise ValueError("Nomes de cenários duplicados ou reservados")
        scenario_names.add(name)
        _resources(scenario["resources"], f"scenario.{name}")


def _totals(lots):
    revenue = sum(x["harvestable_kg"] * x["price_cents_per_kg"] for x in lots)
    cost = sum(x["cost_cents"] for x in lots)
    return {"saleable_kg": sum(x["harvestable_kg"] for x in lots),
            "labor_minutes": sum(x["labor_minutes"] for x in lots),
            "cost_cents": cost, "revenue_cents": revenue,
            "contribution_cents": revenue - cost}


def _violations(lots, totals, resources):
    errors = []
    if any(not x["ready_to_harvest"] for x in lots):
        errors.append("lote_sem_prontidao_confirmada")
    for metric, resource in (("cost_cents", "budget_cents"), ("labor_minutes", "labor_minutes"),
                             ("saleable_kg", "transport_capacity_kg"), ("saleable_kg", "buyer_capacity_kg")):
        if totals[metric] > resources[resource]:
            errors.append(resource)
    return errors


def _solve(lots, resources, objective):
    eligible = sorted((x for x in lots if x["ready_to_harvest"]), key=lambda x: x["id"])
    best, best_totals = [], _totals([])
    secondary = "contribution_cents" if objective == "saleable_kg" else "saleable_kg"
    best_key = (0, 0, 0, 0)
    # The empty plan is feasible and can win when all contributions are negative.
    for n in range(1, len(eligible) + 1):
        for subset in itertools.combinations(eligible, n):
            totals = _totals(subset)
            if _violations(subset, totals, resources):
                continue
            key = (totals[objective], totals[secondary], -totals["cost_cents"], -totals["labor_minutes"])
            if key > best_key:
                best, best_totals, best_key = list(subset), totals, key
    return best, best_totals


def plan(payload):
    validate(payload)
    objective = payload.get("objective", "saleable_kg")
    results = []
    for scenario in [{"name": "base", "resources": payload["resources"]}, *payload.get("scenarios", [])]:
        resources = scenario["resources"]
        selected, totals = _solve(payload["lots"], resources, objective)
        ids = [x["id"] for x in selected]
        baseline = None
        if "baseline_ids" in payload:
            original = [x for x in payload["lots"] if x["id"] in payload["baseline_ids"]]
            original_totals = _totals(original)
            violations = _violations(original, original_totals, resources)
            baseline = {"lot_ids": payload["baseline_ids"], "feasible": not violations,
                        "violations": violations, "estimates": original_totals,
                        "estimated_delta": ({k: totals[k] - original_totals[k]
                                             for k in ("saleable_kg", "contribution_cents", "cost_cents")}
                                            if not violations else None)}
        results.append({"scenario": scenario["name"], "resources": resources,
                        "selected_lot_ids": ids, "estimates": totals,
                        "economic_review_required": any(x["harvestable_kg"] * x["price_cents_per_kg"] < x["cost_cents"] for x in selected),
                        "unused_resources": {"budget_cents": resources["budget_cents"] - totals["cost_cents"],
                                             "labor_minutes": resources["labor_minutes"] - totals["labor_minutes"],
                                             "transport_capacity_kg": resources["transport_capacity_kg"] - totals["saleable_kg"],
                                             "buyer_capacity_kg": resources["buyer_capacity_kg"] - totals["saleable_kg"]},
                        "excluded_lots": [{"id": x["id"], "reason": "prontidao_nao_confirmada" if not x["ready_to_harvest"]
                                           else "fora_da_combinacao_escolhida_para_o_objetivo"}
                                          for x in payload["lots"] if x["id"] not in ids],
                        "baseline_comparison": baseline})
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()
    return {"version": "field-pilot-0.1.0", "status": "experimental_requires_human_approval",
            "data_origin": payload["data_origin"], "planning_date": payload["planning_date"],
            "input_sha256": digest, "objective": objective, "results": results,
            "limitations": ["Planejamento de um dia, lotes indivisíveis, quilos inteiros e capacidade agregada.",
                            "Quantidades, preços e prontidão são entradas; não são previsões do agente.",
                            "Contribuição desconta apenas custos informados; não é lucro líquido.",
                            "Cenários são hipóteses independentes, sem probabilidade atribuída.",
                            "Não calcula ordem, rotas, perecibilidade, clima, manejo nem produtividade biológica.",
                            "Não envia mensagens, contrata, compra, vende ou controla equipamentos.",
                            "Resultado sintético não comprova ganho em propriedade real."]}
