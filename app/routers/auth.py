from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.auth import LoginUsuario, Token
from app.utils import verify_password, create_access_token, get_db, validate_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login(user_credentials: LoginUsuario, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = create_access_token({"user_id": user.id, "email": user.email})

    return Token(access_token=access_token)


@router.post("/refresh-token", response_model=Token)
def refresh_token(current_user: Usuario = Depends(validate_user)):
    access_token = create_access_token(
        {"user_id": current_user.id, "email": current_user.email}
    )
    return Token(access_token=access_token)
