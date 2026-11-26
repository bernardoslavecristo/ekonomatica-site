from copy import deepcopy
from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)

def sample():
    return {'planning_date':'2026-11-26','data_origin':'synthetic',
            'resources':{'budget_cents':30000,'labor_minutes':240,'transport_capacity_kg':200,'buyer_capacity_kg':180},
            'lots':[{'id':n,'harvestable_kg':kg,'labor_minutes':mins,'cost_cents':cost,'price_cents_per_kg':price,'ready_to_harvest':ready}
                    for n,kg,mins,cost,price,ready in [('tomate_A',100,240,9000,400,True),('alface_B',60,180,5000,500,True),('abobrinha_C',80,210,8000,350,True),('tomate_D',120,200,8000,450,False)]],
            'helper':{'available_confirmed':True,'additional_labor_minutes':240,'all_in_cost_cents':10000}}

def test_original_delivery02_acceptance_cases_through_api():
    cases=[(30000,10000,True,'hire_one_helper',46000,15000),
           (50000,30000,True,'keep_without_helper',31000,-5000),
           (50000,25000,True,'keep_without_helper',31000,0),
           (30000,10000,False,'keep_without_helper',31000,None),
           (23999,10000,True,'hire_one_helper',35000,4000),
           (24000,10000,True,'hire_one_helper',46000,15000)]
    for budget,fee,available,decision,contribution,delta in cases:
        s=sample();s['resources']['budget_cents']=budget;s['helper'].update(all_in_cost_cents=fee,available_confirmed=available);before=deepcopy(s)
        response=client.post('/api/kaggriculture/equipe',json=s);assert response.status_code==200
        body=response.json();r=body['result'];chosen=r['chosen_plan']
        assert r['recommendation']==decision and chosen['contribution_after_helper_cents']==contribution
        assert r['incremental_contribution_cents']==delta and 'tomate_D' not in chosen['selected_lot_ids']
        assert s==before and body['stored'] is False and body['integration']['source']=='Kaggriculture Entrega 02'
        assert response.headers['cache-control']=='no-store'
        assert chosen['total_cost_cents']<=budget
        assert chosen['revenue_cents']-chosen['total_cost_cents']==chosen['contribution_after_helper_cents']

def test_budget_availability_and_no_harvest_when_all_lots_unready():
    s=sample();s['resources']['budget_cents']=9900
    r=client.post('/api/kaggriculture/equipe',json=s).json()['result']
    assert not r['with_helper']['feasible'] and r['reason']=='helper_exceeds_upfront_budget'
    s=sample()
    for lot in s['lots']:lot['ready_to_harvest']=False
    r=client.post('/api/kaggriculture/equipe',json=s).json()['result']
    assert r['chosen_plan']['saleable_kg']==0 and r['recommendation']=='keep_without_helper'

def test_transport_bottleneck_makes_extra_labor_unhelpful():
    s=sample();s['resources']['transport_capacity_kg']=100
    r=client.post('/api/kaggriculture/equipe',json=s).json()['result']
    assert r['recommendation']=='keep_without_helper'
    assert r['with_helper']['saleable_kg']<=100 and r['without_helper']['saleable_kg']<=100

def test_invalid_requests_and_duplicate_ids_rejected():
    for change in [lambda s:s['helper'].update(all_in_cost_cents=-1),lambda s:s['helper'].update(available_confirmed='yes'),lambda s:s['lots'][0].update(harvestable_kg=0),lambda s:s['lots'][1].update(id='tomate_A'),lambda s:s.update(data_origin='real_confirmed'),lambda s:s['helper'].update(additional_labor_minutes=1441),lambda s:s.update(lots=s['lots']*3)]:
        s=sample();change(s);assert client.post('/api/kaggriculture/equipe',json=s).status_code==422
