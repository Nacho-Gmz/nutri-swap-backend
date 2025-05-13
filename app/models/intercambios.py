from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Intercambio(Base):
    __tablename__ = "intercambios"

    id = Column(Integer, primary_key=True, index=True)
    alimento_original_id = Column(ForeignKey("alimentos.id"), nullable=False)
    alimento_intercambiado_id = Column(ForeignKey("alimentos.id"), nullable=False)
    usuario_id = Column(ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con alimentos
    alimento_original = relationship("Alimento", foreign_keys=[alimento_original_id])
    alimento_intercambiado = relationship(
        "Alimento", foreign_keys=[alimento_intercambiado_id]
    )

    # Relación con usuario
    usuario = relationship(
        "Usuario", back_populates="intercambios", foreign_keys=[usuario_id]
    )
