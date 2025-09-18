from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    MITIGATED = "MITIGATED"

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

class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    probability: Optional[int] = None
    impact: Optional[int] = None
    status: Optional[RiskStatus] = None
    owner: Optional[str] = None
    mitigation_plan: Optional[str] = None
    category_id: Optional[int] = None

class Risk(RiskBase):
    id: int
    risk_level: RiskLevel
    status: RiskStatus
    recommendations: str  # Nuevo campo para recomendaciones automáticas
    
    class Config:
        orm_mode = True

class RiskWithRecommendations(Risk):
    """Schema extendido con recomendaciones detalladas"""
    detailed_recommendations: Optional[str] = None
    
    class Config:
        orm_mode = True

# Schemas para responses con información adicional
class RiskSummary(BaseModel):
    id: int
    title: str
    risk_level: RiskLevel
    probability: int
    impact: int
    score: int
    owner: str
    status: RiskStatus
    category_name: Optional[str] = None
    
    class Config:
        orm_mode = True

class RiskLevelSummary(BaseModel):
    level: RiskLevel
    count: int
    percentage: float

class DashboardSummary(BaseModel):
    total_risks: int
    risks_by_level: List[RiskLevelSummary]
    critical_risks_count: int
    high_risks_count: int
    recent_risks: List[RiskSummary]

# Schema para estadísticas y reportes
class RiskStats(BaseModel):
    total: int
    open: int
    in_progress: int
    closed: int
    mitigated: int
    by_level: dict

class CategoryStats(BaseModel):
    category_id: int
    category_name: str
    risk_count: int
    average_score: float

# Schema para filtros de búsqueda
class RiskFilter(BaseModel):
    category_id: Optional[int] = None
    risk_level: Optional[RiskLevel] = None
    status: Optional[RiskStatus] = None
    probability_min: Optional[int] = None
    probability_max: Optional[int] = None
    impact_min: Optional[int] = None
    impact_max: Optional[int] = None
    owner: Optional[str] = None

# Schema para recomendaciones personalizadas
class RecommendationRequest(BaseModel):
    probability: int
    impact: int
    risk_level: RiskLevel
    category: Optional[str] = None

class RecommendationResponse(BaseModel):
    risk_level: RiskLevel
    score: int
    general_recommendations: List[str]
    specific_recommendations: List[str]
    urgency_level: str

# Schema para actualización de recomendaciones
class UpdateRecommendationsRequest(BaseModel):
    risk_id: int
    custom_recommendations: Optional[str] = None

class RiskAnalysis(BaseModel):
    risk_id: int
    title: str
    current_level: RiskLevel
    predicted_level: Optional[RiskLevel] = None
    trend: Optional[str] = None  # 'improving', 'worsening', 'stable'
    recommendations: List[str]
    action_plan: Optional[str] = None
