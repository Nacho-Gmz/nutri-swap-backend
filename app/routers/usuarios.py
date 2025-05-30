from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.utils import hash_password, get_db, validate_user

router = APIRouter()


@router.post("/", response_model=UsuarioRead)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    print("************************ANTES******************")
    existing_user = (
        db.query(Usuario).filter(Usuario.correo == usuario_data.correo).first()
    )
    print("************************DESPUES******************")
    if existing_user:
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")

    hashed_pass = hash_password(usuario_data.contraseña)

    new_user = Usuario(
        nombre=usuario_data.nombre,
        apellidos=usuario_data.apellidos,
        correo=usuario_data.correo,
        contraseña=hashed_pass,
        activo=usuario_data.activo,
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
