from pydantic import ConfigDict, BaseModel
from datetime import datetime


class AlimentoBase(BaseModel):
    alimento: str
    categoria: str
    cantidad: float
    unidad: str
    peso_bruto: float
    peso_neto: float
    energia: float
    proteinas: float
    lipidos: float
    carbohidratos: float


class AlimentoRead(AlimentoBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AlimentoNombreId(BaseModel):
    id: int
    alimento: str
    model_config = ConfigDict(from_attributes=True)


class AlimentoSustituto(BaseModel):
    alimento: AlimentoRead
    similitud: float
