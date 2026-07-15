from pydantic import BaseModel

class Marca(BaseModel): # Modelo base
    nombre: str
    descripcion: str | None = "sin descripción"
    id_compania: int

class MarcaPatch(BaseModel): # Modelo para actualizar solo lo necesario (patch).
    nombre: str | None = None
    descripcion: str | None = None
    id_compania: int | None = None

