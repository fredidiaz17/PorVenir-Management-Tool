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

# Modelo oferta_producto

class BaseOfertaProducto(BaseModel):
    id_oferta: int
    id_producto: int

class OfertaProducto(BaseOfertaProducto):
    pass

# Modelo oferta_etiqueta

class BaseOfertaEtiqueta(BaseModel):
    id_oferta: int
    id_etiqueta: int

class OfertaEtiqueta(BaseOfertaEtiqueta):
    pass

# Modelo oferta_marca

class BaseOfertaMarca(BaseModel):
    id_oferta: int
    id_marca: int

class OfertaMarca(BaseOfertaMarca):
    pass

# Modelo oferta_compania

class BaseOfertaCompania(BaseModel):
    id_oferta: int
    id_compania: int

class OfertaCompania(BaseOfertaCompania):
    pass