from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.utils import hash_password, get_db, validate_user

router = APIRouter()


@router.post("/", response_model=UsuarioRead)
def create_user(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current: Usuario = Depends(validate_user)
):
    existing_user = db.query(Usuario).filter(
        Usuario.email == usuario_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="⚠️ Email already registered.")

    hashed_pass = hash_password(usuario_data.password)

    new_user = Usuario(
        nombre=usuario_data.nombre,
        apellidos=usuario_data.apellidos,
        email=usuario_data.email,
        password=hashed_pass,
        active=usuario_data.active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
