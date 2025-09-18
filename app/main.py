from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database import engine, Base
from app.routers import risks, categories
from app import crud, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import FastAPI, Request, Form, Depends

app = FastAPI(
    title="Risk Management API",
    description="API para la gestión de riesgos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente!")



# Incluir routers de API
app.include_router(risks.router)
app.include_router(categories.router)

# Rutas para las vistas HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/risks", response_class=HTMLResponse)
async def risks_page(request: Request, db: Session = Depends(get_db)):
    risks = crud.get_risks(db)
    risks_list = [crud.risk_to_dict(risk) for risk in risks]
    return templates.TemplateResponse("risks.html", {"request": request, "risks": risks_list})

@app.get("/risk/{risk_id}", response_class=HTMLResponse)
async def risk_detail_page(request: Request, risk_id: int, db: Session = Depends(get_db)):
    risk = crud.get_risk(db, risk_id)
    if not risk:
        return RedirectResponse(url="/risks")
    
    return templates.TemplateResponse("risk-detail.html", {
        "request": request,
        "risk": crud.risk_to_dict(risk)
    })

@app.get("/add-risk", response_class=HTMLResponse)
async def add_risk_page(request: Request, db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return templates.TemplateResponse("form.html", {"request": request, "categories": categories})

@app.post("/create-risk", response_class=RedirectResponse)
async def create_risk(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    probability: int = Form(...),
    impact: int = Form(...),
    owner: str = Form(...),
    mitigation_plan: str = Form(""),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    risk_data = schemas.RiskCreate(
        title=title,
        description=description,
        probability=probability,
        impact=impact,
        owner=owner,
        mitigation_plan=mitigation_plan,
        category_id=category_id
    )
    
    crud.create_risk(db, risk_data)
    return RedirectResponse(url="/risks", status_code=303)

@app.get("/risk/{risk_id}", response_class=HTMLResponse)
async def risk_detail_page(request: Request, risk_id: int, db: Session = Depends(get_db)):
    risk = crud.get_risk(db, risk_id)
    if not risk:
        return RedirectResponse(url="/risks")
    
    # Convertir enums a strings para el template
    risk_dict = {
        "id": risk.id,
        "title": risk.title,
        "description": risk.description,
        "probability": risk.probability,
        "impact": risk.impact,
        "risk_level": risk.risk_level,
        "status": risk.status,
        "owner": risk.owner,
        "mitigation_plan": risk.mitigation_plan,
        "recommendations": risk.recommendations,
        "category_id": risk.category_id,
        "created_at": risk.created_at
    }
    
    return templates.TemplateResponse("risk-detail.html", {
        "request": request,
        "risk": risk_dict
    })


# Rutas para las vistas HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/risks", response_class=HTMLResponse)
async def risks_page(request: Request, db: Session = Depends(get_db)):
    risks = crud.get_risks(db)
    # Convertir riesgos a diccionarios para Jinja2
    risks_list = []
    for risk in risks:
        risk_dict = {
            "id": risk.id,
            "title": risk.title,
            "description": risk.description,
            "probability": risk.probability,
            "impact": risk.impact,
            "risk_level": risk.risk_level.value if risk.risk_level else "UNKNOWN",
            "status": risk.status.value if risk.status else "UNKNOWN",
            "owner": risk.owner,
            "mitigation_plan": risk.mitigation_plan,
            "recommendations": risk.recommendations,
            "category_id": risk.category_id,
            "created_at": risk.created_at
        }
        risks_list.append(risk_dict)
    return templates.TemplateResponse("risks.html", {"request": request, "risks": risks_list})

@app.get("/risk/{risk_id}", response_class=HTMLResponse)
async def risk_detail_page(request: Request, risk_id: int, db: Session = Depends(get_db)):
    risk = crud.get_risk(db, risk_id)
    if not risk:
        return RedirectResponse(url="/risks")
    
    # Convertir a diccionario para el template
    risk_dict = {
        "id": risk.id,
        "title": risk.title,
        "description": risk.description,
        "probability": risk.probability,
        "impact": risk.impact,
        "risk_level": risk.risk_level,
        "status": risk.status,
        "owner": risk.owner,
        "mitigation_plan": risk.mitigation_plan,
        "recommendations": risk.recommendations,
        "category_id": risk.category_id,
        "created_at": risk.created_at
    }
    
    return templates.TemplateResponse("risk-detail.html", {
        "request": request,
        "risk": risk_dict
    })

@app.get("/categories-manager", response_class=HTMLResponse)
async def categories_manager(request: Request, db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return templates.TemplateResponse("categories.html", {"request": request, "categories": categories})

@app.post("/create-category", response_class=RedirectResponse)
async def create_category(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    category_data = schemas.RiskCategoryCreate(name=name, description=description)
    crud.create_category(db, category_data)
    return RedirectResponse(url="/categories-manager", status_code=303)

def create_default_categories():
    from app.database import SessionLocal
    from app import crud, schemas
    
    db = SessionLocal()
    try:
        # Verificar si ya existen categorías
        existing_categories = crud.get_categories(db)
        
        if not existing_categories:
            print("Creando categorías por defecto...")
            
            default_categories = [
                {"name": "Tecnológico", "description": "Riesgos relacionados con tecnología y sistemas"},
                {"name": "Operacional", "description": "Riesgos de operaciones y procesos"},
                {"name": "Financiero", "description": "Riesgos económicos y financieros"},
                {"name": "Legal", "description": "Riesgos legales y regulatorios"},
                {"name": "Recursos Humanos", "description": "Riesgos de personal y talento humano"},
                {"name": "Seguridad", "description": "Riesgos de seguridad física y lógica"}
            ]
            
            for category_data in default_categories:
                category = schemas.RiskCategoryCreate(**category_data)
                crud.create_category(db, category)
            
            print("✅ Categorías por defecto creadas exitosamente")
        else:
            print(f"✅ Ya existen {len(existing_categories)} categorías")
            
    except Exception as e:
        print(f"❌ Error creando categorías: {e}")
    finally:
        db.close()