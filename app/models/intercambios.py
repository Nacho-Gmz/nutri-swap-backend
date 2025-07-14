from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Intercambio(Base):
    __tablename__ = "intercambios"

    id = Column(Integer, primary_key=True, index=True)
    original_food_id = Column(ForeignKey("alimentos.id"), nullable=False)
    swapped_food_id = Column(ForeignKey("alimentos.id"), nullable=False)
    user_id = Column(ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con alimentos
    original_food = relationship("Alimento", foreign_keys=[original_food_id])
    swapped_food = relationship("Alimento", foreign_keys=[swapped_food_id])

    # Relación con usuario
    user = relationship("Usuario", back_populates="swaps", foreign_keys=[user_id])
