from pydantic import BaseModel

class BasePreventista(BaseModel):
    nombre: str
    telefono: str | None = "Sin telefono"
    id_compania: int

class Preventista(BasePreventista):
    pass

class PreventistaPatch(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    id_compania: int | None = None
