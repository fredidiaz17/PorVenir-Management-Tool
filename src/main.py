from fastapi import FastAPI
from api.v1.compania import router as compania_router

app = FastAPI() # Punto de entrada 

app.include_router( # Incluir router al app
    compania_router, # Router en cuestión
    prefix="api/v1/compania", # Prefijo de las rutas del router
    tags=["Compañias"] # Agrupación visual en documentación (/docs)
)

