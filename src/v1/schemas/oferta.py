from pydantic import BaseModel
from datetime import datetime
from src.v1.schemas.enums import TipoOferta, EstadoOferta

# Modelo de oferta

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

# Tablas intermedias de Oferta

class BaseOfertaTabla(BaseModel):
    id_oferta: int

# oferta_producto
class OfertaProducto(BaseOfertaTabla):
    id_producto: int

# oferta_etiqueta
class OfertaEtiqueta(BaseOfertaTabla):
    id_etiqueta: int

# oferta_marca
class OfertaMarca(BaseOfertaTabla):
    id_marca: int

# oferta_compania
class OfertaCompania(BaseOfertaTabla):
    id_compania: int
