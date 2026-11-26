"""Stateless API for the Kaggriculture experimental harvesting module."""
from datetime import date, timedelta
from typing import Literal
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from backend.kaggriculture.field_pilot.harvest import plan_week, VERSION

router = APIRouter(prefix='/api/kaggriculture')

class Batch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,20}$')
    quantity: int = Field(strict=True, ge=0, le=100000)
    ready_date: date
    deadline: date

class Order(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(pattern=r'^[A-Za-z0-9_-]{1,20}$')
    quantity: int = Field(strict=True, ge=0, le=100000)
    delivery_date: date

class HarvestRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    start_date: date
    capacity: int = Field(strict=True, ge=0, le=100000)
    fixed: int = Field(strict=True, ge=0, le=100000)
    data_origin: Literal['synthetic', 'user_supplied_estimates']
    batches: list[Batch] = Field(min_length=1, max_length=10)
    orders: list[Order] = Field(min_length=1, max_length=30)

    @model_validator(mode='after')
    def validate_calendar(self):
        if self.start_date > date(9998, 1, 1):
            raise ValueError('Data inicial fora do intervalo permitido.')
        end = self.start_date + timedelta(days=6)
        if any(not self.start_date <= o.delivery_date <= end for o in self.orders):
            raise ValueError('Informe entregas dentro dos sete dias de planejamento.')
        if any(b.deadline < b.ready_date for b in self.batches):
            raise ValueError('O prazo limite deve ser igual ou posterior à data de prontidão.')
        for entries in (self.batches, self.orders):
            if len({e.id for e in entries}) != len(entries):
                raise ValueError('Identificadores duplicados.')
        return self

@router.get('/status')
def status(response: Response):
    response.headers['Cache-Control'] = 'no-store'
    return {'connected': True, 'engine': VERSION, 'competition_policy_connected': False,
            'generative_model_used': False, 'stored': False}

@router.post('/colheita')
def harvest(payload: HarvestRequest, response: Response):
    response.headers['Cache-Control'] = 'no-store'
    try:
        return plan_week(payload.model_dump(mode='json'))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
