from pydantic import BaseModel
from src.schemas.enums import UnidadMedida

class Producto(BaseModel): # Schema para crear un producto
    nombre: str
    stock: int
    precio_compra: float
    unidad_medida: UnidadMedida
    precio_venta: float
    iva: float | None = 0
    id_marca: int