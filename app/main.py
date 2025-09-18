from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import risks, categories

app = FastAPI(
    title="Risk Management API",
    description="API para la gestión de riesgos",
    version="1.0.0"
)

# Configurar CORS para Angular
origins = [
    "http://localhost:4200",    # Angular dev server
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup():
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente!")

app.include_router(risks.router)
app.include_router(categories.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Riesgos"}



