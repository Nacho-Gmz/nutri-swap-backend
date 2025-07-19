from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.intercambios import Intercambio
from app.models.usuarios import Usuario
from app.schemas.intercambios import IntercambioBase
from app.utils import validate_user
from app.database import get_db

router = APIRouter(prefix="/intercambios")


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
    intercambios_usuario = (
        db.query(Intercambio).filter_by(user_id=current_user.id).all()
    )

    if not intercambios_usuario:
        raise HTTPException(status_code=404, detail="No cuenta con intercambios.")

    return intercambios_usuario


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
        original_food_id=intercambio_data.original_food_id,
        swapped_food_id=intercambio_data.swapped_food_id,
        user_id=current_user.id,
    )
    db.add(intercambio)
    db.commit()
    db.refresh(intercambio)
    return intercambio
