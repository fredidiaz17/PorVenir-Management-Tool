from pydantic import BaseModel

class DeudaAbono(BaseModel):
    saldo_pendiente: float


# Pendientes por implementar
class BaseDeuda(BaseModel):
    saldo_pendiente: float | None = 0.0
    estado: bool = True
    id_cliente: int


class DeudaPatch(BaseModel):
    saldo_pendiente: float | None = None
    estado: bool | None = None
    id_cliente: int | None = None
