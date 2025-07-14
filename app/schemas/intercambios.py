from pydantic import BaseModel


class IntercambioBase(BaseModel):
    original_food_id: int
    swapped_food_id: int
