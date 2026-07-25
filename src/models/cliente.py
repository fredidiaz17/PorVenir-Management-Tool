from __future__ import annotations # Con esto se evita el import circular
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.deuda import DeudaModel
    from src.models.venta import VentaModel

class ClienteModel(Base):
    __tablename__ = "cliente"
    
    id_cliente: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)


    # Relación con deudas
    deudas: Mapped[DeudaModel] = relationship(
        "DeudaModel", 
        back_populates="cliente", 
        cascade="all, delete-orphan"
    )

    # Relación con ventas
    ventas: Mapped[list[VentaModel]] = relationship(
        "VentaModel", 
        back_populates="cliente", 
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"ClienteModel(id_cliente={self.id_cliente}, nombre={self.nombre}, telefono={self.telefono})" 
