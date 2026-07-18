from pydantic import BaseModel
from datetime import date
from src.v1.schemas.enums import EstadoPedido

class BasePedido(BaseModel):
    fecha_pedido: date 
    estado: EstadoPedido | None = EstadoPedido.PENDIENTE
    subtotal: float 
    impuestos: float | None = 0.0
    total: float 
    id_preventista: int 

class Pedido(BasePedido):
    pass

class PedidoPatch(BaseModel):
    fecha_pedido: date | None = None
    estado: EstadoPedido | None = None
    subtotal: float | None = None
    impuestos: float | None = None
    total: float | None = None
    id_preventista: int | None = None
