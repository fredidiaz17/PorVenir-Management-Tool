from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.venta import VentaModel
    from src.models.producto import ProductoModel

class DetalleVentaModel(Base):
    __tablename__ = "detalle_venta"
    
    id_venta: Mapped[int] = mapped_column(ForeignKey("venta.id_venta", ondelete="CASCADE"), primary_key=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("producto.id_producto" ), primary_key=True)
    cantidad: Mapped[float] = mapped_column(Float)
    precio_venta: Mapped[float] = mapped_column(Float)
    descuento_manual: Mapped[float] = mapped_column(Float)
    subtotal: Mapped[float] = mapped_column(Float)

    venta: Mapped[VentaModel] = relationship(
        "VentaModel",
        back_populates="detalle_venta"
    )

    producto: Mapped[ProductoModel] = relationship(
        "ProductoModel",
        back_populates="detalle_venta"
    )

    def __repr__(self) -> str:
        return f"DetalleVentaModel(id_venta={self.id_venta!r}, id_producto={self.id_producto!r}, cantidad={self.cantidad!r})"
