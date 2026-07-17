from pydantic import BaseModel

class BaseDetallePedido(BaseModel):
    cantidad: float 
    precio_unitario: float 
    subtotal_linea: float 
    iva_porcentaje: float | None = 0.0
    iva_valor: float | None = 0.0
    total_linea: float

class DetallePedido(BaseDetallePedido):
    id_pedido: int
    id_producto: int

class DetallePedidoPatch(BaseModel):
    cantidad: float | None = None
    precio_unitario: float | None = None
    subtotal_linea: float | None = None
    iva_porcentaje: float | None = None
    iva_valor: float | None = None
    total_linea: float | None = None
