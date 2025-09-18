from sqlalchemy.orm import Session
from . import models, schemas

def get_risk_recommendations(risk_level: schemas.RiskLevel, probability: int, impact: int) -> str:
    """
    Genera recomendaciones automáticas basadas en el nivel de riesgo,
    probabilidad e impacto.
    """
    score = probability * impact
    
    recommendations = {
        schemas.RiskLevel.LOW: [
            "Monitoreo periódico del riesgo",
            "Documentar en registro de riesgos",
            "Revisar en reuniones trimestrales"
        ],
        schemas.RiskLevel.MEDIUM: [
            "Asignar responsable específico",
            "Definir plan de acción con fechas",
            "Monitoreo mensual",
            "Establecer indicadores de control",
            "Reportar en reuniones mensuales"
        ],
        schemas.RiskLevel.HIGH: [
            "Plan de mitigación inmediato",
            "Asignar recursos específicos",
            "Monitoreo semanal",
            "Reporte directo a gerencia",
            "Definir triggers de escalamiento",
            "Evaluar transferencia del riesgo (seguros)"
        ],
        schemas.RiskLevel.CRITICAL: [
            "¡Acción inmediata requerida!",
            "Escalar a comité de crisis",
            "Asignar presupuesto especial",
            "Monitoreo diario",
            "Plan de contingencia activado",
            "Comunicación constante con stakeholders",
            "Considerar evitación del riesgo"
        ]
    }
    
    # Recomendaciones base según el nivel
    base_recommendations = recommendations.get(risk_level, [])
    
    # Recomendaciones adicionales basadas en características específicas
    additional_recommendations = []
    
    if probability >= 4:
        additional_recommendations.append("Implementar controles preventivos inmediatos")
    
    if impact >= 4:
        additional_recommendations.append("Desarrollar plan de contingencia detallado")
    
    if score > 15:
        additional_recommendations.append("Realizar análisis de root cause")
    
    # Combinar todas las recomendaciones
    all_recommendations = base_recommendations + additional_recommendations
    
    return "; ".join(all_recommendations)




def calculate_risk_level(probability: int, impact: int) -> schemas.RiskLevel:
    score = probability * impact
    if score <= 4:
        return schemas.RiskLevel.LOW
    elif score <= 10:
        return schemas.RiskLevel.MEDIUM
    elif score <= 20:
        return schemas.RiskLevel.HIGH
    else:
        return schemas.RiskLevel.CRITICAL

def create_risk(db: Session, risk: schemas.RiskCreate):
    risk_level = calculate_risk_level(risk.probability, risk.impact)
    db_risk = models.Risk(
        **risk.dict(),
        risk_level=risk_level,
        status=models.RiskStatus.OPEN
    )
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk

def get_risks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Risk).offset(skip).limit(limit).all()

def get_risk(db: Session, risk_id: int):
    return db.query(models.Risk).filter(models.Risk.id == risk_id).first()

def update_risk(db: Session, risk_id: int, risk_update: schemas.RiskUpdate):
    db_risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()
    if not db_risk:
        return None
    
    update_data = risk_update.dict(exclude_unset=True)
    
    # Recalculate risk level if probability or impact changes
    if 'probability' in update_data or 'impact' in update_data:
        new_prob = update_data.get('probability', db_risk.probability)
        new_impact = update_data.get('impact', db_risk.impact)
        update_data['risk_level'] = calculate_risk_level(new_prob, new_impact)
    
    for field, value in update_data.items():
        setattr(db_risk, field, value)
    
    db.commit()
    db.refresh(db_risk)
    return db_risk

def delete_risk(db: Session, risk_id: int):
    db_risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()
    if db_risk:
        db.delete(db_risk)
        db.commit()
    return db_risk

# Similar CRUD functions for RiskCategory...

# CRUD operations for RiskCategory
def create_category(db: Session, category: schemas.RiskCategoryCreate):
    db_category = models.RiskCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RiskCategory).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(models.RiskCategory).filter(models.RiskCategory.id == category_id).first()

def update_category(db: Session, category_id: int, category_update: schemas.RiskCategoryCreate):
    db_category = db.query(models.RiskCategory).filter(models.RiskCategory.id == category_id).first()
    if not db_category:
        return None
    
    for field, value in category_update.dict().items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.RiskCategory).filter(models.RiskCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category