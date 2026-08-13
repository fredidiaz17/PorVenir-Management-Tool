from pydantic import BaseModel, ConfigDict

class BaseDetalleVenta(BaseModel):
    cantidad: float 
    precio_venta: float
    descuento_manual: float | None = 0.0
    subtotal: float

    # Para convertir modelo ORM a dict
    model_config = ConfigDict(from_attributes= True)
    
class CreateDetalleVenta(BaseDetalleVenta):
    id_producto: int

class UpdateDetalleVenta(BaseDetalleVenta):
    pass

class DetalleVentaPatch(BaseModel):
    cantidad: float | None = None
    precio_venta: float | None = None
    descuento_manual: float | None = None
    subtotal: float | None = None
