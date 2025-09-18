from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./risk_management.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Importar los modelos DESPUÉS de definir Base
# Esto asegura que SQLAlchemy los registre correctamente
from app.models import RiskCategory, Risk

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()