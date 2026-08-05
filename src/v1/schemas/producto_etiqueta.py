from pydantic import BaseModel

class BaseProductoEtiqueta(BaseModel):
    estado: str | None = "Inactivo"

class ProductoEtiqueta(BaseProductoEtiqueta):
    id_producto: int
    id_etiqueta: int

