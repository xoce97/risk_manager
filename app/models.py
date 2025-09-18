from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Importar Base desde database.py
import enum

class RiskLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskStatus(enum.Enum):
    OPEN = "OPEN"         # Cambiado de "abierto" a "OPEN"
    ENPROGRESS = "IN-PROGRESS"  #Cambiado de "inprogress" a "IN-PROGRESS"
    CIERRA = "CLOSED"      #Cambiado de "cerrado" a "CLOSED"
    MITIGATED = "MITIGATED"    #Cambiado de "mitigado" un "MITIGATED"

class RiskCategory(Base):
    __tablename__ = "risk_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(500))
    
    risks = relationship("Risk", back_populates="category")

class Risk(Base):
    __tablename__ = "risks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(String(1000))
    probability = Column(Integer)  # 1-5 scale
    impact = Column(Integer)       # 1-5 scale
    risk_level = Column(Enum(RiskLevel))
    status = Column(Enum(RiskStatus), default=RiskStatus.OPEN)
    owner = Column(String(100))
    mitigation_plan = Column(String(1000))
    recommendations = Column(String(1000))  # ← Nuevo campo para recomendaciones
    
    category_id = Column(Integer, ForeignKey("risk_categories.id"))
    category = relationship("RiskCategory", back_populates="risks")