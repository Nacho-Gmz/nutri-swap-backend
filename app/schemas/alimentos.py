from pydantic import ConfigDict, BaseModel
from datetime import datetime


class AlimentoBase(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str
    gross_weight: float
    net_weight: float
    calories: float
    protein: float
    lipids: float
    carbohydrates: float


class AlimentoRead(AlimentoBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AlimentoNombreId(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class AlimentoSustituto(BaseModel):
    alimento: AlimentoRead
    similitud: float
