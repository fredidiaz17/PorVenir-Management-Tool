from pydantic import BaseModel

class Cliente(BaseModel): # Modelo base
    nombre: str
    telefono: str | None = "No proporcionado"

class ClientePatch(BaseModel): # Modelo para actualizar solo lo necesario (patch).
    nombre: str | None = None
    telefono: str | None = None
    

