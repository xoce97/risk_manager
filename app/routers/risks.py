from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db


router = APIRouter(prefix="/risks", tags=["risks"])



@router.post("/", response_model=schemas.Risk)
def create_risk(risk: schemas.RiskCreate, db: Session = Depends(get_db)):
    return crud.create_risk(db=db, risk=risk)

@router.get("/", response_model=List[schemas.Risk])
def read_risks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    risks = crud.get_risks(db, skip=skip, limit=limit)
    return risks

@router.get("/{risk_id}", response_model=schemas.Risk)
def read_risk(risk_id: int, db: Session = Depends(get_db)):
    db_risk = crud.get_risk(db, risk_id=risk_id)
    if db_risk is None:
        raise HTTPException(status_code=404, detail="Risk not found")
    return db_risk

@router.put("/{risk_id}", response_model=schemas.Risk)
def update_risk(risk_id: int, risk_update: schemas.RiskUpdate, db: Session = Depends(get_db)):
    db_risk = crud.update_risk(db, risk_id=risk_id, risk_update=risk_update)
    if db_risk is None:
        raise HTTPException(status_code=404, detail="Risk not found")
    return db_risk

@router.delete("/{risk_id}")
def delete_risk(risk_id: int, db: Session = Depends(get_db)):
    db_risk = crud.delete_risk(db, risk_id=risk_id)
    if db_risk is None:
        raise HTTPException(status_code=404, detail="Risk not found")
    return {"message": "Risk deleted successfully"}

@router.get("/{risk_id}/recommendations", response_model=schemas.RiskWithRecommendations)
def get_risk_recommendations(risk_id: int, db: Session = Depends(get_db)):
    db_risk = crud.get_risk(db, risk_id=risk_id)
    if db_risk is None:
        raise HTTPException(status_code=404, detail="Risk not found")
    
    # Generar recomendaciones detalladas
    detailed_recommendations = crud.get_detailed_recommendations(
        db_risk.risk_level, db_risk.probability, db_risk.impact
    )
    
    return {
        **db_risk.__dict__,
        "detailed_recommendations": detailed_recommendations
    }