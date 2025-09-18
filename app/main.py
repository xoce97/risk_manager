from fastapi import FastAPI
from app.database import engine, Base
from app.routers import risks, categories

app = FastAPI(
    title="Risk Management API",
    description="API para la gestión de riesgos",
    version="1.0.0"
)

# Mover la creación de tablas al evento de startup
@app.on_event("startup")
def on_startup():
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente!")

# Incluir routers
app.include_router(risks.router)
app.include_router(categories.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Riesgos"}