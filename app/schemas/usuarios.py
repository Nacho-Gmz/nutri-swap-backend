from pydantic import ConfigDict, BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    correo: EmailStr
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioRead(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
