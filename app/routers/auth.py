from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.auth import LoginUsuario, Token
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.utils import (
    hash_password,
    verify_password,
    create_access_token,
    validate_user,
)
from app.database import get_db

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UsuarioRead)
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
        active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user_credentials: LoginUsuario, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña no válidos.",
        )

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña no válidos.",
        )

    access_token = create_access_token({"user_id": user.id, "email": user.email})

    return Token(access_token=access_token)


@router.post("/refresh-token", response_model=Token)
def refresh_token(current_user: Usuario = Depends(validate_user)):
    access_token = create_access_token(
        {"user_id": current_user.id, "email": current_user.email}
    )
    return Token(access_token=access_token)
