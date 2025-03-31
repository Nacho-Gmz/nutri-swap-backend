from pydantic import ConfigDict, BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    active: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioRead(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
