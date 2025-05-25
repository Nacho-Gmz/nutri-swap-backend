from sqlalchemy import Column, Integer, String, DateTime, func, Float
from ..database import Base


class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    alimento = Column(String(100), nullable=False)
    categoria = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(100), nullable=False)
    peso_bruto = Column(Float, nullable=False)
    peso_neto = Column(Float, nullable=False)
    energia = Column(Float, nullable=False)
    proteinas = Column(Float, nullable=False)
    lipidos = Column(Float, nullable=False)
    carbohidratos = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    #updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
