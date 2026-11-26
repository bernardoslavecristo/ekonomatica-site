"""Compare zero or one temporary helper using the existing whole-lot planner.

Synthetic decision support: costs and minutes are supplied, never inferred.
No booking, legal employment advice, API call or Kaggle simulator integration.
"""

import copy
import hashlib
import json

from .planner import plan


def evaluate_helper(payload, helper):
    """Maximize one day's contribution after the helper's all-inclusive cost.

    A helper adds aggregate labor capacity only. Transport and buyer capacity
    stay fixed. The fee must be funded before sales and is charged in full.
    Break-even favors the plan without hiring. Input objects are preserved.
    """
    base = copy.deepcopy(payload)
    baseline = plan(base)  # Reuse all existing validation and optimization.
    if base.get("objective", "saleable_kg") != "contribution_cents":
        raise ValueError("Use objective=contribution_cents para comparar contratação")
    if base.get("scenarios"):
        raise ValueError("Compare uma entrada de um dia por vez; use scenarios=[]")
    keys = {"available_confirmed", "additional_labor_minutes", "all_in_cost_cents"}
    if not isinstance(helper, dict) or set(helper) != keys:
        raise ValueError(f"helper deve conter exatamente {sorted(keys)}")
    if type(helper["available_confirmed"]) is not bool:
        raise ValueError("available_confirmed deve ser booleano")
    for key in keys - {"available_confirmed"}:
        if type(helper[key]) is not int or helper[key] < 0:
            raise ValueError(f"{key} deve ser um inteiro não negativo")
    if helper["additional_labor_minutes"] == 0:
        raise ValueError("additional_labor_minutes deve ser maior que zero")

    def summarize(result, fee):
        totals = result["estimates"]
        return {
            "feasible": True,
            "selected_lot_ids": result["selected_lot_ids"],
            "saleable_kg": totals["saleable_kg"],
            "labor_minutes_used": totals["labor_minutes"],
            "lot_cost_cents": totals["cost_cents"],
            "helper_cost_cents": fee,
            "total_cost_cents": totals["cost_cents"] + fee,
            "revenue_cents": totals["revenue_cents"],
            "contribution_after_helper_cents": totals["contribution_cents"] - fee,
            "unused_resources": copy.deepcopy(result["unused_resources"]),
        }

    without = summarize(baseline["results"][0], 0)
    with_helper = {"feasible": False, "reason": "availability_not_confirmed"}
    fee = helper["all_in_cost_cents"]
    if helper["available_confirmed"]:
        if fee > base["resources"]["budget_cents"]:
            with_helper["reason"] = "helper_exceeds_upfront_budget"
        else:
            adjusted = copy.deepcopy(base)
            adjusted["resources"]["budget_cents"] -= fee
            adjusted["resources"]["labor_minutes"] += helper["additional_labor_minutes"]
            with_helper = summarize(plan(adjusted)["results"][0], fee)

    delta = (with_helper["contribution_after_helper_cents"] - without["contribution_after_helper_cents"]
             if with_helper["feasible"] else None)
    hire = delta is not None and delta > 0
    reason = ("positive_incremental_contribution" if hire else
              with_helper["reason"] if delta is None else
              "break_even_keep_without_helper" if delta == 0 else
              "lower_contribution_with_helper")
    digest = hashlib.sha256(json.dumps({"payload": payload, "helper": helper},
                                       sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()
    return {
        "version": "field-pilot-helper-0.1.0",
        "status": "experimental_requires_human_approval",
        "data_origin": base["data_origin"],
        "planning_date": base["planning_date"],
        "objective": "contribution_after_helper_cents",
        "input_sha256": digest,
        "without_helper": without,
        "with_helper": with_helper,
        "incremental_contribution_cents": delta,
        "recommendation": "hire_one_helper" if hire else "keep_without_helper",
        "reason": reason,
        "chosen_plan": copy.deepcopy(with_helper if hire else without),
        "limitations": [
            "Apenas zero ou um ajudante, por um dia, com custo total informado.",
            "Minutos são capacidade agregada; não modela escala, rotas ou dependências de tarefas.",
            "Custos dos lotes devem excluir a diária, para não descontá-la duas vezes.",
            "Contribuição desconta só os custos informados; não é lucro líquido.",
            "Preços, prontidão, disponibilidade e produção são entradas, não previsões.",
            "Não contrata pessoas nem comprova retorno numa propriedade real.",
            "Não executa ações do ambiente Kaggle nem usa modelos Meta nesta etapa.",
        ],
    }
