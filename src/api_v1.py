# Router unificador de sub Routers 
# El único router que interactúa directamente con el servidor (main.py)

from fastapi import APIRouter
from .routers.v1.compania import router as compania_router
from .routers.v1.marca import router as marca_router
from .routers.v1.producto import router as producto_router
router = APIRouter()

# Incluir routers de modulos
router.include_router(compania_router, prefix="/compania", tags=["Compañias"])
router.include_router(
    marca_router, 
    prefix="/marca", 
    tags=["Marcas"] # Agrupación visual en documentación (/docs)
)
router.include_router(
    producto_router, 
    prefix="/producto", 
    tags=["Productos"] # Agrupación visual en documentación (/docs)
)