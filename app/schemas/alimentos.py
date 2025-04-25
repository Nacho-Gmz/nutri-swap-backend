from pydantic import ConfigDict, BaseModel, PydanticUserError
from datetime import datetime


class AlimentoBase(BaseModel):
    alimento : str
    categoria : str
    cantidad :float
    unidad : str
    peso_bruto : float
    peso_neto : float
    energia : float
    proteinas : float
    lipidos : float
    carbohidratos : float
    updated_at : datetime


class AlimentoRead(AlimentoBase):
    id : int
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)



class AlimentoNombreId(BaseModel):
    alimento : str
    id : int
    model_config = ConfigDict(from_attributes=True)