from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.utils import hash_password, validate_user
from app.database import get_db

router = APIRouter(prefix="/usuarios")


@router.post("/", response_model=UsuarioRead)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")

    hashed_pass = hash_password(usuario_data.password)

    new_user = Usuario(
        firstName=usuario_data.firstName,
        lastName=usuario_data.lastName,
        email=usuario_data.email,
        password=hashed_pass,
        active=usuario_data.active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[UsuarioRead])
def list_users(
    db: Session = Depends(get_db), usuario_actual: Usuario = Depends(validate_user)
):
    return db.query(Usuario).all()
