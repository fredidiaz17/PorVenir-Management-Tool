from pydantic import BaseModel
from datetime import date
from src.v1.schemas.enums import MedioPago
from src.v1.schemas.detalle_venta import DetalleVenta

class BaseVenta(BaseModel):
    fecha: date 
    medio_pago: MedioPago | None = MedioPago.EFECTIVO
    total: float 
    id_cliente: int 

class Venta(BaseVenta):
    detalles_venta: list[DetalleVenta]

class VentaPatch(BaseModel):
    fecha: date | None = None
    medio_pago: MedioPago | None = None
    total: float | None = None
    id_cliente: int | None = None
