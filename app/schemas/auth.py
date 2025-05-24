from pydantic import BaseModel, EmailStr


class LoginUsuario(BaseModel):
    correo: EmailStr
    contraseña: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
