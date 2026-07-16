from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.producto_etiqueta import ProductoEtiquetaModel

class EtiquetaModel(Base):
    __tablename__ = "etiqueta"
    
    id_etiqueta: Mapped[int] = mapped_column(primary_key=True)
    nombre_etiqueta: Mapped[str] = mapped_column(String(50))
    descripcion_etiqueta: Mapped[str] = mapped_column(String)
    color_hex: Mapped[str] = mapped_column(String(9))

    # Relación con ProductoEtiquetaModel
    producto_etiquetas: Mapped[list[ProductoEtiquetaModel]] = relationship(
        "ProductoEtiquetaModel",
        back_populates="etiqueta",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"EtiquetaModel(id_etiqueta={self.id_etiqueta!r}, nombre_etiqueta={self.nombre_etiqueta!r})"
