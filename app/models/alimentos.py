from sqlalchemy import Column, Integer, String, DateTime, func, Float
from ..database import Base


class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(100), nullable=False)
    gross_weight = Column(Float, nullable=False)
    net_weight = Column(Float, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    lipids = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
