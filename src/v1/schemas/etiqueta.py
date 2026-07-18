from pydantic import BaseModel

class BaseEtiqueta(BaseModel):
    nombre_etiqueta: str
    descripcion_etiqueta: str | None = "sin descripción"
    color_hex: str | None = "#000000"

class Etiqueta(BaseEtiqueta):
    pass

class EtiquetaPatch(BaseModel):
    nombre_etiqueta: str | None = None
    descripcion_etiqueta: str | None = None
    color_hex: str | None = None
