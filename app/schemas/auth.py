from pydantic import BaseModel, EmailStr


class LoginUsuario(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
