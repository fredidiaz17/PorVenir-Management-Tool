from pydantic import BaseModel
from src.v1.schemas.enums import UnidadMedida

class BaseProducto(BaseModel): # Schema de comun productos
    cantidad_stock: float | None = 0.0
    unidad_medida: UnidadMedida | None = UnidadMedida.UNIDADES
    porcentaje_iva: float | None = 0.0

class Producto(BaseProducto): # Schema para crear un producto o actualizarlo completamente.
    nombre: str
    precio_compra: float
    precio_venta: float
    id_marca: int

class ProductoPatch(BaseModel): 
    """Schema para actualizar un producto."""
    nombre: str | None = None
    precio_compra: float | None = None
    precio_venta: float | None = None
    id_marca: int | None = None    

