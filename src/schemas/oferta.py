from pydantic import BaseModel
from datetime import datetime
from src.schemas.enums import TipoOferta, EstadoOferta

class BaseOferta(BaseModel):
    nombre: str
    descripcion: str 
    tipo_oferta: TipoOferta
    valor_descuento: float 
    cantidad_minima: int
    producto_regalo: int 
    fecha_inicio: datetime 
    fecha_fin: datetime 
    estado: EstadoOferta = EstadoOferta.ACTIVA

class Oferta(BaseOferta):
    pass

class OfertaPatch(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    tipo_oferta: TipoOferta | None = None
    valor_descuento: float | None = None
    cantidad_minima: int | None = None
    producto_regalo: int | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    estado: EstadoOferta | None = None
