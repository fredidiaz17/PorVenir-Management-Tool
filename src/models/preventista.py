from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.compania import CompaniaModel
    from src.models.pedido import PedidoModel

class PreventistaModel(Base):
    __tablename__ = "preventista"
    
    id_preventista: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    id_compania: Mapped[int] = mapped_column(ForeignKey("compania.id_compania", ondelete= "CASCADE" ))

    compania: Mapped[CompaniaModel] = relationship(
        "CompaniaModel",
        back_populates="preventistas"
    )

    pedidos: Mapped[list[PedidoModel]] = relationship(
        "PedidoModel",
        back_populates="preventista",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"PreventistaModel(id_preventista={self.id_preventista!r}, nombre={self.nombre!r})"
