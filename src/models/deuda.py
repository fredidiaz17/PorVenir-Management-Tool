from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.cliente import ClienteModel

class DeudaModel(Base):
    __tablename__ = "deuda"
    
    id_deuda: Mapped[int] = mapped_column(primary_key=True)
    saldo_pendiente: Mapped[float | None] = mapped_column(Float, default=0.0)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente", ondelete="CASCADE"), unique=True)

    cliente: Mapped[ClienteModel] = relationship(
        "ClienteModel",
        back_populates="deudas"
    )

    def __repr__(self) -> str:
        return f"DeudaModel(id_deuda={self.id_deuda!r}, saldo_pendiente={self.saldo_pendiente!r})"
