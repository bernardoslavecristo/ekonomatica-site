from copy import deepcopy
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
def sample():
    return {'start_date':'2026-11-26','capacity':160,'fixed':100,'data_origin':'synthetic',
            'batches':[{'id':name,'quantity':q,'ready_date':r,'deadline':e} for name,q,r,e in
                       [('A',250,'2026-11-26','2026-11-28'),('B',320,'2026-11-28','2026-11-30'),('C',260,'2026-11-30','2026-12-02')]],
            'orders':[{'id':f'P{i+1}','quantity':q,'delivery_date':d} for i,(q,d) in enumerate(zip(
                [60,150,80,140,100,160,70],['2026-11-26','2026-11-27','2026-11-28','2026-11-29','2026-11-30','2026-12-01','2026-12-02']))]}

def test_sample_dates_conservation_and_explanations():
    s=sample();before=deepcopy(s);r=client.post('/api/kaggriculture/colheita',json=s)
    assert r.status_code==200
    result=r.json();assert result['planned']['totals']['delivered']==760
    assert result['baseline']['totals']['delivered']==610
    assert result['integration']['connected'] and not result['integration']['competition_policy_connected']
    assert result['stored'] is False and r.headers['cache-control']=='no-store'
    assert s==before and len(result['input_sha256'])==64
    for name in ['planned','baseline']:
        run=result[name];t=run['totals']
        assert t['production']==t['delivered']+t['loss']+t['remaining']
        assert t['demand']==t['delivered']+t['shortage']
        for d in run['days']:
            assert d['harvested']<=s['capacity'] and d['explanations']
            for picked in d['picked']:
                batch=next(b for b in s['batches'] if b['id']==picked['batch'])
                assert batch['ready_date']<=d['date']<=batch['deadline']

def test_same_day_orders_allocated_without_double_counting():
    s=sample();s['capacity']=100;s['orders'][1]['delivery_date']=s['orders'][0]['delivery_date']
    result=client.post('/api/kaggriculture/colheita',json=s).json()
    assert result['orders'][0]['delivered']==60 and result['orders'][1]['delivered']==40
    assert sum(o['delivered'] for o in result['orders'])==result['planned']['totals']['delivered']
    assert result['planned']['days'][0]['shortage']==110
    assert any('Capacidade' in x for x in result['planned']['days'][0]['explanations'])

def test_zero_capacity_and_zero_demand():
    for empty in ['capacity','orders','batches']:
        s=sample()
        if empty=='capacity':s['capacity']=0
        else:
            for entry in s[empty]:entry['quantity']=0
        r=client.post('/api/kaggriculture/colheita',json=s)
        assert r.status_code==200 and r.json()['planned']['totals']['delivered']==0

def test_invalid_constraints_rejected():
    for mutate in [lambda s:s.update(capacity=-1),lambda s:s.update(capacity=1.5),lambda s:s.update(capacity=True),
                   lambda s:s['orders'][0].update(delivery_date='2026-12-03'),
                   lambda s:s['batches'][0].update(deadline='2026-11-25'),
                   lambda s:s['batches'][1].update(id='A'),lambda s:s.update(data_origin='confirmed_real')]:
        s=sample();mutate(s);assert client.post('/api/kaggriculture/colheita',json=s).status_code==422

def test_late_stock_is_preserved_and_expired_stock_cannot_be_harvested():
    s=sample();s['batches'][0]['ready_date']='2026-11-20';s['batches'][0]['deadline']='2026-11-25'
    s['batches'][2]['deadline']='2026-12-10'
    r=client.post('/api/kaggriculture/colheita',json=s).json()['planned']
    assert not any(p['batch']=='A' for d in r['days'] for p in d['picked'])
    assert r['days'][0]['expired']==250 and r['totals']['remaining']>0
    t=r['totals'];assert t['production']==t['delivered']+t['loss']+t['remaining']
