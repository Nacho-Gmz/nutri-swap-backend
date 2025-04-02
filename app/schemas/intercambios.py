from pydantic import ConfigDict, BaseModel


class IntercambioBase(BaseModel):
    alimento_original_id: int
    alimento_intercambiado_id: int
