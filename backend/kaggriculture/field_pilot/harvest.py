"""Weekly lettuce extension of field_pilot. Units: heads, not kilograms.

This explicit-constraint agent is independent of the competition's trained
policy. No agronomic inference, storage, external actions or model API calls.
The original whole-lot planner remains unchanged in planner.py.
"""
from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json

VERSION = 'kaggriculture-harvest-0.2.0'


def plan_week(payload):
    start = date.fromisoformat(payload['start_date'])
    end = start + timedelta(days=6)
    demand = [0] * 7
    for order in payload['orders']:
        delivery = date.fromisoformat(order['delivery_date'])
        if not start <= delivery <= end:
            raise ValueError('As entregas devem estar dentro da semana de planejamento.')
        demand[(delivery - start).days] += order['quantity']
    for batch in payload['batches']:
        if date.fromisoformat(batch['ready_date']) > date.fromisoformat(batch['deadline']):
            raise ValueError('O prazo limite de um canteiro não pode ser anterior à prontidão.')

    def run(planned):
        stock = [{**b, 'remaining': b['quantity']} for b in deepcopy(payload['batches'])]
        days = []
        for index, wanted in enumerate(demand):
            current = (start + timedelta(days=index)).isoformat()
            expired_before = sum(b['remaining'] for b in stock if b['deadline'] < current)
            for b in stock:
                if b['deadline'] < current:
                    b['remaining'] = 0
            ready = sorted((b for b in stock if b['ready_date'] <= current <= b['deadline']),
                           key=lambda b: (b['deadline'], b['id']))
            available = sum(b['remaining'] for b in ready)
            target = min(payload['capacity'], wanted if planned else payload['fixed'])
            left = target
            picked = []
            for b in ready:
                quantity = min(left, b['remaining'])
                if quantity:
                    picked.append({'batch': b['id'], 'quantity': quantity, 'deadline': b['deadline']})
                    b['remaining'] -= quantity
                    left -= quantity
            harvested = sum(b['quantity'] for b in picked)
            delivered = min(harvested, wanted)
            losses = []
            expired = expired_before
            for b in stock:
                if b['deadline'] == current and b['remaining']:
                    losses.append({'batch': b['id'], 'quantity': b['remaining']})
                    expired += b['remaining']
                    b['remaining'] = 0
            shortage = wanted - delivered
            reasons = []
            if wanted == 0:
                reasons.append('Sem pedidos para esta data; o plano não indica colheita para estocar.')
            elif picked:
                reasons.append('Prioridade ao prazo limite mais próximo: ' + ', '.join(
                    f"{b['batch']} ({b['quantity']} pés, limite {b['deadline']})" for b in picked) + '.')
            if shortage:
                if payload['capacity'] < wanted:
                    reasons.append(f"Capacidade diária: {payload['capacity']} pés para {wanted} pedidos.")
                if available < wanted:
                    reasons.append(f"Produção pronta nesta data: {available} pés para {wanted} pedidos; lotes fora da janela não entram.")
            if losses:
                reasons.append('Saldo no dia limite: ' + ', '.join(f"{b['batch']}: {b['quantity']} pés" for b in losses) + '.')
            days.append({'day': index + 1, 'date': current, 'demand': wanted, 'picked': picked,
                         'harvested': harvested, 'delivered': delivered, 'shortage': shortage,
                         'excess': harvested - delivered, 'expired': expired,
                         'loss': harvested - delivered + expired,
                         'available': available, 'explanations': reasons})
        keys = ('demand', 'harvested', 'delivered', 'shortage', 'excess', 'expired', 'loss')
        totals = {k: sum(d[k] for d in days) for k in keys}
        totals.update(production=sum(b['quantity'] for b in stock), remaining=sum(b['remaining'] for b in stock))
        return {'days': days, 'totals': totals}

    baseline, planned = run(False), run(True)
    # Requests sharing a date consume that day's delivery in their displayed order.
    remaining = {d['date']: d['delivered'] for d in planned['days']}
    orders = []
    for order in payload['orders']:
        assigned = min(order['quantity'], remaining[order['delivery_date']])
        remaining[order['delivery_date']] -= assigned
        orders.append({**order, 'delivered': assigned, 'shortage': order['quantity'] - assigned})
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()
    return {'baseline': baseline, 'planned': planned, 'orders': orders,
            'integration': {'connected': True, 'engine': VERSION, 'method': 'explicit_constraints',
                            'competition_policy_connected': False, 'generative_model_used': False},
            'data_origin': payload['data_origin'], 'input_sha256': hashlib.sha256(encoded).hexdigest(),
            'stored': False,
            'limitations': ['Dados informados e resultados simulados; sem validação de produtividade em campo.',
                            'Sem estoque pós-colheita; pedidos faltantes não passam ao dia seguinte.',
                            'Regra diária por prazo limite, não otimização global da semana.',
                            'Política treinada da competição e previsões agronômicas não conectadas.']}
