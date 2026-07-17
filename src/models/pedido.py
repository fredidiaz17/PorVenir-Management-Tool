from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date
from sqlalchemy import ForeignKey, Float, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.schemas.enums import EstadoPedido

if TYPE_CHECKING:
    from src.models.preventista import PreventistaModel
    

class PedidoModel(Base):
    __tablename__ = "pedido"
    
    id_pedido: Mapped[int] = mapped_column(primary_key=True)
    fecha_pedido: Mapped[date] = mapped_column(Date)
    estado: Mapped[EstadoPedido | None] = mapped_column(SQLEnum(EstadoPedido), default=EstadoPedido.PENDIENTE)
    subtotal: Mapped[float] = mapped_column(Float)
    impuestos: Mapped[float | None] = mapped_column(Float, default=0.0)
    total: Mapped[float] = mapped_column(Float)
    id_preventista: Mapped[int] = mapped_column(ForeignKey("preventista.id_preventista", ondelete="CASCADE"))

    preventista: Mapped[PreventistaModel] = relationship(
        "PreventistaModel",
        back_populates="pedidos"
    )


    def __repr__(self) -> str:
        return f"PedidoModel(id_pedido={self.id_pedido!r}, fecha_pedido={self.fecha_pedido!r}, estado={self.estado!r})"
