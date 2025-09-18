from sqlalchemy.orm import Session
from . import models, schemas

def calculate_risk_level(probability: int, impact: int) -> schemas.RiskLevel:
    """
    Calcula el nivel de riesgo basado en probabilidad e impacto.
    Formula: Puntuación = Probabilidad × Impacto
    """
    score = probability * impact
    if score <= 4:
        return schemas.RiskLevel.LOW
    elif score <= 10:
        return schemas.RiskLevel.MEDIUM
    elif score <= 20:
        return schemas.RiskLevel.HIGH
    else:
        return schemas.RiskLevel.CRITICAL

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
            "Revisar en reuniones trimestrales",
            "Mantener en observación"
        ],
        schemas.RiskLevel.MEDIUM: [
            "Asignar responsable específico",
            "Definir plan de acción con fechas límite",
            "Monitoreo mensual del riesgo",
            "Establecer indicadores de control (KPIs)",
            "Reportar en reuniones mensuales de equipo",
            "Evaluar controles preventivos"
        ],
        schemas.RiskLevel.HIGH: [
            "Plan de mitigación inmediato requerido",
            "Asignar recursos y presupuesto específicos",
            "Monitoreo semanal con reportes ejecutivos",
            "Reporte directo a gerencia y stakeholders",
            "Definir triggers de escalamiento claro",
            "Evaluar transferencia del riesgo (seguros)",
            "Desarrollar plan de contingencia detallado"
        ],
        schemas.RiskLevel.CRITICAL: [
            "¡Acción inmediata requerida!",
            "Escalar a comité de crisis o directiva",
            "Asignar presupuesto de emergencia",
            "Monitoreo diario con reportes ejecutivos",
            "Plan de contingencia activado inmediatamente",
            "Comunicación constante con todos los stakeholders",
            "Considerar evitación completa del riesgo",
            "Reuniones diarias de seguimiento"
        ]
    }
    
    # Recomendaciones base según el nivel
    base_recommendations = recommendations.get(risk_level, [])
    
    # Recomendaciones adicionales basadas en características específicas
    additional_recommendations = []
    
    if probability >= 4:
        additional_recommendations.extend([
            "Implementar controles preventivos inmediatos",
            "Aumentar frecuencia de monitoreo",
            "Capacitar equipo en procedimientos de emergencia"
        ])
    
    if impact >= 4:
        additional_recommendations.extend([
            "Desarrollar plan de contingencia detallado",
            "Identificar recursos alternativos",
            "Establecer comunicaciones de crisis"
        ])
    
    if score > 15:
        additional_recommendations.append("Realizar análisis de root cause completo")
    
    if probability == 5 and impact == 5:
        additional_recommendations.extend([
            "Activación inmediata de protocolo de crisis",
            "Notificación a autoridades si aplica",
            "Asignación de equipo dedicado full-time"
        ])
    
    # Combinar todas las recomendaciones
    all_recommendations = base_recommendations + additional_recommendations
    
    return "; ".join(all_recommendations)

def get_detailed_recommendations(risk_level: schemas.RiskLevel, probability: int, impact: int) -> str:
    """
    Genera recomendaciones más detalladas y formateadas para respuestas específicas
    """
    score = probability * impact
    
    urgency_levels = {
        schemas.RiskLevel.LOW: "BAJA URGENCIA",
        schemas.RiskLevel.MEDIUM: "URGENCIA MODERADA",
        schemas.RiskLevel.HIGH: "ALTA URGENCIA",
        schemas.RiskLevel.CRITICAL: "URGENCIA CRÍTICA"
    }
    
    detailed_recommendations = f"""
ANÁLISIS DE RIESGO - RECOMENDACIONES ESPECÍFICAS
=============================================

NIVEL DE RIESGO: {risk_level.value}
PUNTAJE: {score} (Probabilidad: {probability}/5 × Impacto: {impact}/5)
NIVEL DE URGENCIA: {urgency_levels.get(risk_level, 'NO DEFINIDO')}

RECOMENDACIONES PRINCIPALES:
----------------------------
"""
    
    if risk_level == schemas.RiskLevel.LOW:
        detailed_recommendations += """
• Monitoreo trimestral mediante checklist
• Mantener documentación en registro oficial
• Revisar en reuniones de equipo mensuales
• Evaluar en revisiones periódicas de proceso
"""
    elif risk_level == schemas.RiskLevel.MEDIUM:
        detailed_recommendations += """
• Asignar responsable específico con autoridad
• Desarrollar plan de acción con cronograma de 30 días
• Monitoreo mensual con reportes formales
• Establecer KPIs de control específicos
• Incluir en reportes de gestión mensuales
"""
    elif risk_level == schemas.RiskLevel.HIGH:
        detailed_recommendations += """
• Plan de mitigación a implementar en máximo 7 días
• Asignar recursos dedicados y presupuesto
• Monitoreo semanal con reportes ejecutivos
• Comunicación directa con alta gerencia
• Desarrollar plan de contingencia operativo
• Evaluar opciones de transferencia de riesgo
"""
    elif risk_level == schemas.RiskLevel.CRITICAL:
        detailed_recommendations += """
• ACCIÓN INMEDIATA REQUERIDA (menos de 48 horas)
• Activación de comité de crisis
• Presupuesto de emergencia asignado
• Monitoreo diario con reportes horarios si es necesario
• Plan de contingencia activado inmediatamente
• Comunicación constante con stakeholders clave
• Considerar parada de operaciones si aplica
"""

    # Recomendaciones adicionales basadas en score
    if score > 18:
        detailed_recommendations += """
RECOMENDACIONES ADICIONALES POR ALTO PUNTAJE:
---------------------------------------------
• Reunión urgente con comité directivo
• Evaluar parar actividades relacionadas temporalmente
• Notificar a autoridades regulatorias si aplica
• Activar plan de comunicación de crisis
"""

    if probability >= 4:
        detailed_recommendations += """
CONTROLES PREVENTIVOS RECOMENDADOS:
-----------------------------------
• Implementar controles preventivos inmediatos
• Aumentar frecuencia de auditorías
• Capacitación intensiva del personal
• Redundancia en sistemas críticos
"""

    detailed_recommendations += f"""
PRÓXIMOS PASOS SUGERIDOS:
-------------------------
1. Revisar y priorizar recomendaciones
2. Asignar responsables y fechas límite
3. Establecer sistema de monitoreo
4. Programar seguimiento en { '30 días' if risk_level == schemas.RiskLevel.LOW else '15 días' if risk_level == schemas.RiskLevel.MEDIUM else '7 días' if risk_level == schemas.RiskLevel.HIGH else '24 horas' }
5. Documentar lecciones aprendidas
"""

    return detailed_recommendations

# CRUD operations for Risk
def create_risk(db: Session, risk: schemas.RiskCreate):
    risk_level = calculate_risk_level(risk.probability, risk.impact)
    recommendations = get_risk_recommendations(risk_level, risk.probability, risk.impact)
    
    db_risk = models.Risk(
        **risk.dict(),
        risk_level=risk_level,
        status=models.RiskStatus.OPEN,
        recommendations=recommendations  # ← Guardamos las recomendaciones
    )
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk

def get_risks(db: Session, skip: int = 0, limit: int = 100, filters: dict = None):
    """
    Obtiene todos los riesgos con filtros opcionales
    """
    query = db.query(models.Risk)
    
    if filters:
        if filters.get('category_id'):
            query = query.filter(models.Risk.category_id == filters['category_id'])
        if filters.get('risk_level'):
            query = query.filter(models.Risk.risk_level == filters['risk_level'])
        if filters.get('status'):
            query = query.filter(models.Risk.status == filters['status'])
        if filters.get('probability_min'):
            query = query.filter(models.Risk.probability >= filters['probability_min'])
        if filters.get('probability_max'):
            query = query.filter(models.Risk.probability <= filters['probability_max'])
        if filters.get('owner'):
            query = query.filter(models.Risk.owner.ilike(f"%{filters['owner']}%"))
    
    return query.offset(skip).limit(limit).all()

def get_risk(db: Session, risk_id: int):
    """
    Obtiene un riesgo específico por ID
    """
    return db.query(models.Risk).filter(models.Risk.id == risk_id).first()

def update_risk(db: Session, risk_id: int, risk_update: schemas.RiskUpdate):
    db_risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()
    if not db_risk:
        return None
    
    update_data = risk_update.dict(exclude_unset=True)
    
    # Recalcular si cambia probabilidad o impacto
    if 'probability' in update_data or 'impact' in update_data:
        new_prob = update_data.get('probability', db_risk.probability)
        new_impact = update_data.get('impact', db_risk.impact)
        new_risk_level = calculate_risk_level(new_prob, new_impact)
        update_data['risk_level'] = new_risk_level
        update_data['recommendations'] = get_risk_recommendations(
            new_risk_level, new_prob, new_impact
        )
    
    for field, value in update_data.items():
        setattr(db_risk, field, value)
    
    db.commit()
    db.refresh(db_risk)
    return db_risk

def delete_risk(db: Session, risk_id: int):
    """
    Elimina un riesgo existente
    """
    db_risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()
    if db_risk:
        db.delete(db_risk)
        db.commit()
    return db_risk

def update_risk_recommendations(db: Session, risk_id: int, custom_recommendations: str = None):
    """
    Actualiza las recomendaciones de un riesgo, opcionalmente con recomendaciones personalizadas
    """
    db_risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()
    if not db_risk:
        return None
    
    if custom_recommendations:
        # Usar recomendaciones personalizadas
        db_risk.recommendations = custom_recommendations
    else:
        # Recalcular recomendaciones automáticas
        new_recommendations = get_risk_recommendations(
            db_risk.risk_level, db_risk.probability, db_risk.impact
        )
        db_risk.recommendations = new_recommendations
    
    db.commit()
    db.refresh(db_risk)
    return db_risk

# CRUD operations for RiskCategory
def create_category(db: Session, category: schemas.RiskCategoryCreate):
    """
    Crea una nueva categoría de riesgo
    """
    db_category = models.RiskCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todas las categorías de riesgo
    """
    return db.query(models.RiskCategory).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    """
    Obtiene una categoría específica por ID
    """
    return db.query(models.RiskCategory).filter(models.RiskCategory.id == category_id).first()

def update_category(db: Session, category_id: int, category_update: schemas.RiskCategoryCreate):
    """
    Actualiza una categoría existente
    """
    db_category = db.query(models.RiskCategory).filter(models.RiskCategory.id == category_id).first()
    if not db_category:
        return None
    
    for field, value in category_update.dict().items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    """
    Elimina una categoría existente
    """
    db_category = db.query(models.RiskCategory).filter(models.RiskCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# Funciones adicionales para análisis y reportes
def get_risk_stats(db: Session):
    """
    Obtiene estadísticas generales de riesgos
    """
    total = db.query(models.Risk).count()
    open_count = db.query(models.Risk).filter(models.Risk.status == models.RiskStatus.OPEN).count()
    in_progress_count = db.query(models.Risk).filter(models.Risk.status == models.RiskStatus.IN_PROGRESS).count()
    closed_count = db.query(models.Risk).filter(models.Risk.status == models.RiskStatus.CLOSED).count()
    mitigated_count = db.query(models.Risk).filter(models.Risk.status == models.RiskStatus.MITIGATED).count()
    
    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress_count,
        "closed": closed_count,
        "mitigated": mitigated_count
    }

def get_risks_by_level(db: Session):
    """
    Obtiene conteo de riesgos por nivel
    """
    return db.query(
        models.Risk.risk_level,
        db.func.count(models.Risk.id)
    ).group_by(models.Risk.risk_level).all()