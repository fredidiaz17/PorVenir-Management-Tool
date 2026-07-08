from fastapi import FastAPI
from src.api.v1.compania import router as compania_router

app = FastAPI(
    title = "PorvenirMGT API",
    description = "Aplicación web que permite a tiendas gestionar su inventario de productos.",
    version = "1.0.0"
) # Punto de entrada 

app.include_router( # Incluir router al app
    compania_router, # Router en cuestión
    prefix="/api/v1/compania", # Prefijo de las rutas del router
    tags=["Compañias"] # Agrupación visual en documentación (/docs)
)

