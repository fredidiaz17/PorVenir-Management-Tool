# Router unificador de sub Routers 
# El único router que interactúa directamente con el servidor (main.py)

from fastapi import APIRouter
from .routers.v1.compania import router as compania_router
from .routers.v1.marca import router as marca_router
from .routers.v1.producto import router as producto_router
from .routers.v1.etiqueta import router as etiqueta_router
from .routers.v1.oferta import router as oferta_router
from .routers.v1.producto_etiqueta import router as producto_etiqueta_router
from .routers.v1.preventista import router as preventista_router
from .routers.v1.pedido import router as pedido_router
from .routers.v1.detalle_pedido import router as detalle_pedido_router

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
router.include_router(
    etiqueta_router, 
    prefix="/etiqueta", 
    tags=["Etiquetas"]
)
router.include_router(
    oferta_router, 
    prefix="/oferta", 
    tags=["Ofertas"]
)
router.include_router(
    producto_etiqueta_router, 
    prefix="/producto_etiqueta", 
    tags=["Producto Etiquetas"]
)
router.include_router(
    preventista_router, 
    prefix="/preventista", 
    tags=["Preventistas"]
)
router.include_router(
    pedido_router, 
    prefix="/pedido", 
    tags=["Pedidos"]
)
router.include_router(
    detalle_pedido_router, 
    prefix="/detalle_pedido", 
    tags=["Detalle Pedidos"]
)