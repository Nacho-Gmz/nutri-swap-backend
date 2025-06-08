from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.alimentos import Alimento
from app.schemas.alimentos import (
    AlimentoNombreId,
    AlimentoRead,
    AlimentoBase,
    AlimentoSustituto,
)
from app.utils import get_db
from app.ia import obtener_sustitutos_ordenados

router = APIRouter()


# Crear un nuevo alimento
@router.post("/", response_model=AlimentoRead)
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


# Obtener todos los alimentos
@router.get("/", response_model=List[AlimentoRead])
def obtener_todos_alimentos(db: Session = Depends(get_db)):
    alimentos = db.query(Alimento).all()
    if not alimentos:
        raise HTTPException(status_code=404, detail="Alimentos no encontrados")
    return alimentos


# Obtener nombres de todos los alimentos
@router.get("/nombres", response_model=List[AlimentoNombreId])
def obtener_nombres_alimentos(db: Session = Depends(get_db)):
    nombres = db.query(Alimento.id, Alimento.alimento).all()
    if not nombres:
        raise HTTPException(status_code=404, detail="Alimentos no encontrados")
    # Extraer solo los nombres de la lista de tuplas
    return [nombre for nombre in nombres]


# Obtener datos de un alimento basado en su id
@router.get("/{id}", response_model=AlimentoRead)
def obtener_alimento_por_id(id: int, db: Session = Depends(get_db)):
    alimento = db.query(Alimento).filter(Alimento.id == id).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento


# Obtener datos de un alimento basado en su nombre
# @router.get("/{alimento_nombre}", response_model=AlimentoRead)
# def obtener_alimento_por_nombre(alimento_nombre: str, db: Session = Depends(get_db)):
#     alimento = db.query(Alimento).filter(Alimento.alimento == alimento_nombre).first()
#     if not alimento:
#         raise HTTPException(status_code=404, detail="Alimento no encontrado")
#     return alimento


# eliminar alimento pasando su id
@router.delete("/{id}")
def eliminar_alimento(id: int, db: Session = Depends(get_db)):
    alimento = db.query(Alimento).filter(Alimento.id == id).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    db.delete(alimento)
    db.commit()
    return {"mensaje": "Alimento eliminado correctamente"}


# Actualizar alimento
@router.put("/{id}", response_model=AlimentoRead)
def actualizar_alimento(
    id: int,
    datos_actualizados: AlimentoBase,
    db: Session = Depends(get_db),
):
    alimento = db.query(Alimento).filter(Alimento.id == id).first()
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


# Obtener lista de alimentos de la misma categoria dando el id de un alimento
@router.get("/categoria/{id}", response_model=List[AlimentoRead])
def obtener_alimentos_misma_categoria(id: str, db: Session = Depends(get_db)):
    alimento_base = db.query(Alimento).filter(Alimento.id == id).first()
    if not alimento_base:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    alimentos = (
        db.query(Alimento)
        .filter(Alimento.categoria == alimento_base.categoria, Alimento.id != id)
        .all()
    )
    return alimentos


@router.get("/ia/{id}", response_model=List[AlimentoSustituto])
def obtener_alimentos_ia(id: str, db: Session = Depends(get_db)):
    alimento_base = db.query(Alimento).filter(Alimento.id == id).first()
    if not alimento_base:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    alimentos = (
        db.query(Alimento).filter(Alimento.categoria == alimento_base.categoria).all()
    )
    lista_aliementos = obtener_sustitutos_ordenados(alimento_base, alimentos)
    resultado = []
    for alimento, similitud in lista_aliementos:
        resultado.append(
            AlimentoSustituto(
                alimento=AlimentoRead.model_validate(alimento),
                similitud=float(similitud),
            )
        )
    return resultado
