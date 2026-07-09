from fastapi import FastAPI
from src.api_v1 import router as api_v1_router

app = FastAPI(
    title = "PorvenirMGT API",
    description = "Aplicación web que permite a tiendas gestionar su inventario de productos.",
    version = "1.0.0"
) # Punto de entrada 

app.include_router( # Incluir router al app
    api_v1_router, # Router en cuestión
    prefix="/api/v1", # Prefijo de las rutas del router
)

