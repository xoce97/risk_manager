# Importar los routers para facilitar el acceso
from .risks import router as risks_router
from .categories import router as categories_router

# Lista de todos los routers disponibles
__all__ = ["risks_router", "categories_router"]