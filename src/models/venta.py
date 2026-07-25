from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date
from sqlalchemy import ForeignKey, Float, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.v1.schemas.enums import MedioPago

if TYPE_CHECKING:
    from src.models.cliente import ClienteModel
    from src.models.detalle_venta import DetalleVentaModel

class VentaModel(Base):
    __tablename__ = "venta"
    
    id_venta: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date] = mapped_column(Date)
    medio_pago: Mapped[MedioPago] = mapped_column(SQLEnum(MedioPago))
    total: Mapped[float] = mapped_column(Float)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente", ondelete="CASCADE"))

    cliente: Mapped[ClienteModel] = relationship(
        "ClienteModel",
        back_populates="ventas"
    )

    detalles: Mapped[list[DetalleVentaModel]] = relationship(
        "DetalleVentaModel",
        back_populates="venta",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"VentaModel(id_venta={self.id_venta!r}, fecha={self.fecha!r}, medio_pago={self.medio_pago!r})"
