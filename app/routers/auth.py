from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.auth import LoginUsuario, Token
from app.schemas.usuarios import UsuarioCreate, UsuarioRead
from app.utils import (
    hash_password,
    verify_password,
    create_access_token,
    get_db,
    validate_user,
)

router = APIRouter()


@router.post("/signup", response_model=UsuarioRead)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(Usuario).filter(Usuario.correo == usuario_data.correo).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="⚠️ Correo ya registrado.")

    hashed_pass = hash_password(usuario_data.contraseña)

    new_user = Usuario(
        nombre=usuario_data.nombre,
        apellidos=usuario_data.apellidos,
        correo=usuario_data.correo,
        contraseña=hashed_pass,
        activo=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user_credentials: LoginUsuario, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == user_credentials.correo).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña no válidos.",
        )

    if not verify_password(user_credentials.contraseña, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña no válidos.",
        )

    access_token = create_access_token({"user_id": user.id, "email": user.correo})

    return Token(access_token=access_token)


@router.post("/refresh-token", response_model=Token)
def refresh_token(current_user: Usuario = Depends(validate_user)):
    access_token = create_access_token(
        {"user_id": current_user.id, "email": current_user.correo}
    )
    return Token(access_token=access_token)
