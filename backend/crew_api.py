"""Bounded stateless interface to the existing field_pilot labor decision engine."""
from datetime import date
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from backend.kaggriculture.field_pilot.labor import evaluate_helper

router = APIRouter(prefix='/api/kaggriculture')

class Resources(BaseModel):
    model_config = ConfigDict(extra='forbid')
    budget_cents: int = Field(strict=True, ge=0, le=100000000)
    labor_minutes: int = Field(strict=True, ge=0, le=10080)
    transport_capacity_kg: int = Field(strict=True, ge=0, le=100000)
    buyer_capacity_kg: int = Field(strict=True, ge=0, le=100000)

class Lot(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,30}$')
    harvestable_kg: int = Field(strict=True, ge=1, le=100000)
    labor_minutes: int = Field(strict=True, ge=0, le=10080)
    cost_cents: int = Field(strict=True, ge=0, le=100000000)
    price_cents_per_kg: int = Field(strict=True, ge=0, le=1000000)
    ready_to_harvest: bool = Field(strict=True)

class Helper(BaseModel):
    model_config = ConfigDict(extra='forbid')
    available_confirmed: bool = Field(strict=True)
    additional_labor_minutes: int = Field(strict=True, gt=0, le=1440)
    all_in_cost_cents: int = Field(strict=True, ge=0, le=100000000)

class CrewRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    planning_date: date
    data_origin: Literal['synthetic','user_supplied_estimates']
    resources: Resources
    lots: list[Lot] = Field(min_length=1, max_length=8)
    helper: Helper

@router.post('/equipe')
def crew(data: CrewRequest, response: Response):
    response.headers['Cache-Control'] = 'no-store'
    supplied = data.model_dump(mode='json')
    helper = supplied.pop('helper')
    supplied['objective'] = 'contribution_cents'
    supplied['scenarios'] = []
    try:
        result = evaluate_helper(supplied, helper)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
    return {'result':result, 'stored':False,
            'integration':{'connected':True,'engine':'field-pilot-helper-0.1.0',
                           'source':'Kaggriculture Entrega 02', 'trained_policy_connected':False}}
