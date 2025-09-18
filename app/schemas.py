from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    MITIGATED = "mitigated"

class RiskCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class RiskCategoryCreate(RiskCategoryBase):
    pass

class RiskCategory(RiskCategoryBase):
    id: int
    
    class Config:
        orm_mode = True

class RiskBase(BaseModel):
    title: str
    description: str
    probability: int
    impact: int
    owner: str
    mitigation_plan: Optional[str] = None
    category_id: int

class RiskCreate(RiskBase):
    pass

class Risk(RiskBase):
    id: int
    risk_level: RiskLevel
    status: RiskStatus
    recommendations: str  # ← Nuevo campo para recomendaciones
    
    class Config:
        orm_mode = True

class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    probability: Optional[int] = None
    impact: Optional[int] = None
    status: Optional[RiskStatus] = None
    owner: Optional[str] = None
    mitigation_plan: Optional[str] = None
    category_id: Optional[int] = None


class RiskWithRecommendations(Risk):
    """Schema extendido con recomendaciones detalladas"""
    detailed_recommendations: Optional[str] = None