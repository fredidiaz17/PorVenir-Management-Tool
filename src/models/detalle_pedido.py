from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.pedido import PedidoModel
    from src.models.producto import ProductoModel

class DetallePedidoModel(Base):
    __tablename__ = "detalle_pedido"
    
    id_pedido: Mapped[int] = mapped_column(ForeignKey("pedido.id_pedido", ondelete="CASCADE"), primary_key=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("producto.id_producto", ondelete="CASCADE"), primary_key=True)
    cantidad: Mapped[float] = mapped_column(Float)
    precio_unitario: Mapped[float] = mapped_column(Float)
    subtotal_linea: Mapped[float] = mapped_column(Float)
    iva_porcentaje: Mapped[float | None] = mapped_column(Float, default=0.0)
    iva_valor: Mapped[float | None] = mapped_column(Float, default= 0.0)
    total_linea: Mapped[float] = mapped_column(Float)

    pedido: Mapped[PedidoModel] = relationship(
        "PedidoModel",
        back_populates="detalles"
    )

    producto: Mapped[ProductoModel] = relationship(
        "ProductoModel",
        back_populates="detalles_pedido"
    )

    def __repr__(self) -> str:
        return f"DetallePedidoModel(id_pedido={self.id_pedido!r}, id_producto={self.id_producto!r}, cantidad={self.cantidad!r})"
