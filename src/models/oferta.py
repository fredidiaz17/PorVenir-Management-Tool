from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Enum as SQLEnum, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.v1.schemas.enums import TipoOferta, EstadoOferta

if TYPE_CHECKING:
    from src.models.producto import ProductoModel
    from src.models.etiqueta import EtiquetaModel
    from src.models.marca import MarcaModel
    from src.models.compania import CompaniaModel

# Modelos de tablas intermedia de oferta

oferta_producto = Table(
    "oferta_producto",
    Base.metadata,
    Column("id_oferta", Integer, ForeignKey("oferta.id_oferta", ondelete="CASCADE"), primary_key=True),
    Column("id_producto", Integer, ForeignKey("producto.id_producto", ondelete="CASCADE"), primary_key=True)
)

oferta_etiqueta = Table(
    "oferta_etiqueta",
    Base.metadata,
    Column("id_oferta", Integer, ForeignKey("oferta.id_oferta", ondelete="CASCADE"), primary_key=True),
    Column("id_etiqueta", Integer, ForeignKey("etiqueta.id_etiqueta", ondelete="CASCADE"), primary_key=True)
)

oferta_marca = Table(
    "oferta_marca",
    Base.metadata,
    Column("id_oferta", Integer, ForeignKey("oferta.id_oferta", ondelete="CASCADE"), primary_key=True),
    Column("id_marca", Integer, ForeignKey("marca.id_marca", ondelete="CASCADE"), primary_key=True)
)

oferta_compania = Table(
    "oferta_compania",
    Base.metadata,
    Column("id_oferta", Integer, ForeignKey("oferta.id_oferta", ondelete="CASCADE"), primary_key=True),
    Column("id_compania", Integer, ForeignKey("compania.id_compania", ondelete="CASCADE"), primary_key=True)
)

class OfertaModel(Base):
    __tablename__ = "oferta"
    
    id_oferta: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(String)
    tipo_oferta: Mapped[TipoOferta] = mapped_column(SQLEnum(TipoOferta))
    valor_descuento: Mapped[float] = mapped_column(Float)
    cantidad_minima: Mapped[int] = mapped_column(Integer, default=1)
    producto_regalo: Mapped[int] = mapped_column(Integer)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime)
    fecha_fin: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[EstadoOferta] = mapped_column(SQLEnum(EstadoOferta), default=EstadoOferta.ACTIVA)

    # Relaciones
    # NOTA: Se eliminó el cascade "all, delete-orphan" de las relaciones de oferta con sus entidades relacionadas, 
    # ya que se eliminaría la oferta al eliminar una de sus entidades relacionadas.
    # NO es recomendado usarlo en relaciones N:M
    productos: Mapped[list["ProductoModel"]] = relationship(
        secondary="oferta_producto",
        back_populates="ofertas",
    )

    etiquetas: Mapped[list["EtiquetaModel"]] = relationship(
        secondary="oferta_etiqueta",
        back_populates="ofertas",
        
    )

    marcas: Mapped[list["MarcaModel"]] = relationship(
        secondary="oferta_marca",
        back_populates="ofertas",
    )

    companias: Mapped[list["CompaniaModel"]] = relationship(
        secondary="oferta_compania",
        back_populates="ofertas",
    )

    def __repr__(self) -> str:
        return f"OfertaModel(id_oferta={self.id_oferta!r}, nombre={self.nombre!r})"  
