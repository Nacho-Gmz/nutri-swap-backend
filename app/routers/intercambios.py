from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.intercambios import Intercambio
from app.models.usuarios import Usuario
from app.schemas.intercambios import IntercambioBase
from app.utils import validate_user, get_db

router = APIRouter()


@router.get("/{id}")
def obtener_intercambios(
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(validate_user),
):
    """
    Retorna un objeto JSON con:
      - intercambios: lista de intercambios
      - total: total de intercambios
      - page: página actual
      - pages: total de páginas
    """
    return db.query(Intercambio).filter_by(usuario_id=current_user.id).all()


# Crear un nuevo intercambio
@router.post("/{id}", status_code=201)
def crear_intercambio(
    intercambio_data: IntercambioBase,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(validate_user),
):
    """
    Recibe un objeto JSON con:
      - alimento_original
      - alimento_intercambiado
      - usuario_id
    """
    intercambio = Intercambio(
        alimento_original_id=intercambio_data.alimento_original_id,
        alimento_intercambiado_id=intercambio_data.alimento_intercambiado_id,
        usuario_id=current_user.id,
    )
    db.add(intercambio)
    db.commit()
    db.refresh(intercambio)
    return intercambio
