from pydantic import ConfigDict, BaseModel, EmailStr


class UsuarioBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    active: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioRead(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
