from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.alimentos import Alimento
from app.schemas.alimentos import AlimentoRead, AlimentoBase
from app.utils import get_db

router = APIRouter()


# Obtener datos de un alimento basado en su id
@router.get("/alimento/{id}", response_model=AlimentoRead)
def obtener_alimento_por_id(id: int, db: Session = Depends(get_db)):
    alimento = db.query(Alimento).filter(Alimento.id == id).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento


# Obtener datos de un alimento basado en su nombre
@router.get("/alimento/{alimento_nombre}", response_model=AlimentoRead)
def obtener_alimento_por_nombre(alimento_nombre: str, db: Session = Depends(get_db)):
    alimento = db.query(Alimento).filter(Alimento.alimento == alimento_nombre).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento


@router.post("/alimento", response_model=AlimentoRead)
def crear_alimento(
    alimento_data: AlimentoRead,
    db: Session = Depends(get_db),
):
    aliemento_existente = (
        db.query(Alimento).filter(Alimento.alimento == alimento_data.alimento).first()
    )
    if aliemento_existente:
        raise HTTPException(status_code=400, detail="⚠️ Alimento ya registrado.")

    nuevo_alimento = Alimento(
        alimento=alimento_data.alimento,
        categoria=alimento_data.categoria,
        cantidad=alimento_data.cantidad,
        unidad=alimento_data.unidad,
        peso_bruto=alimento_data.peso_bruto,
        peso_neto=alimento_data.peso_neto,
        energia=alimento_data.energia,
        proteinas=alimento_data.proteinas,
        lipidos=alimento_data.lipidos,
        carbohidratos=alimento_data.carbohidratos,
        created_at=alimento_data.created_at,
        updated_at=alimento_data.updated_at,
    )
    db.add(nuevo_alimento)
    db.commit()
    db.refresh(nuevo_alimento)
    return nuevo_alimento


# eliminar alimento pasando su id
@router.delete("/alimento/{alimento_nombre}")
def eliminar_alimento(alimento_nombre: str, db: Session = Depends(get_db)):
    alimento = db.query(Alimento).filter(Alimento.alimento == alimento_nombre).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    db.delete(alimento)
    db.commit()
    return {"mensaje": "Alimento eliminado correctamente"}


# Actualizar alimento
@router.put("/alimento/{alimento_nombre}", response_model=AlimentoRead)
def actualizar_alimento(
    alimento_nombre: int,
    datos_actualizados: AlimentoBase,
    db: Session = Depends(get_db),
):
    alimento = db.query(Alimento).filter(Alimento.alimento == alimento_nombre).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    alimento.alimento = datos_actualizados.alimento
    alimento.categoria = datos_actualizados.categoria
    alimento.cantidad = datos_actualizados.cantidad
    alimento.unidad = datos_actualizados.unidad
    alimento.peso_bruto = datos_actualizados.peso_bruto
    alimento.peso_neto = datos_actualizados.peso_neto
    alimento.energia = datos_actualizados.energia
    alimento.proteinas = datos_actualizados.proteinas
    alimento.lipidos = datos_actualizados.lipidos
    alimento.carbohidratos = datos_actualizados.carbohidratos
    alimento.updated_at = datos_actualizados.updated_at

    db.commit()
    db.refresh(alimento)
    return alimento


# Obtener todos los alimentos
@router.get("/alimentos", response_model=List[AlimentoRead])
def obtener_todos_alimentos(db: Session = Depends(get_db)):
    alimentos = db.query(Alimento)
    if not alimentos:
        raise HTTPException(status_code=404, detail="Alimentos no encontrados")
    return alimentos


# Obtener lista de alimentos de la misma categoria dando el nombre de un alimento
@router.get("/alimentos/categoria/{nombre}", response_model=List[AlimentoRead])
def obtener_alimentos_misma_categoria(nombre: str, db: Session = Depends(get_db)):
    alimento_base = db.query(Alimento).filter(Alimento.alimento == nombre).first()
    if not alimento_base:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    alimentos = (
        db.query(Alimento)
        .filter(
            Alimento.categoria == alimento_base.categoria, Alimento.alimento != nombre
        )
        .all()
    )
    return alimentos
