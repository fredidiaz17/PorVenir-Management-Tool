from pydantic import BaseModel
from src.v1.schemas.enums import EstadoOferta

class BaseProductoEtiqueta(BaseModel):
    estado: EstadoOferta | None = EstadoOferta.ACTIVO

class ProductoEtiqueta(BaseProductoEtiqueta):
    id_producto: int
    id_etiqueta: int

