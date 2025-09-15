from pydantic import BaseModel


class IntercambioAlimentosRead(BaseModel):
    original_food: dict  # {id, name}
    swapped_food: dict  # {id, name}
