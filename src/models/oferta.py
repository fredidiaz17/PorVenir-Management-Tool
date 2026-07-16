from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.schemas.enums import TipoOferta, EstadoOferta


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

    def __repr__(self) -> str:
        return f"OfertaModel(id_oferta={self.id_oferta!r}, nombre={self.nombre!r})"
