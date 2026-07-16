from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.schemas.enums import EstadoRegistro

if TYPE_CHECKING:
    from src.models.producto import ProductoModel
    from src.models.etiqueta import EtiquetaModel

class ProductoEtiquetaModel(Base):
    __tablename__ = "producto_etiqueta"
    
    id_producto: Mapped[int] = mapped_column(ForeignKey("producto.id_producto", ondelete="CASCADE"), primary_key=True)
    id_etiqueta: Mapped[int] = mapped_column(ForeignKey("etiqueta.id_etiqueta", ondelete="CASCADE"), primary_key=True)
    estado: Mapped[EstadoRegistro] = mapped_column(SQLEnum(EstadoRegistro), default=EstadoRegistro.ACTIVO)

    producto: Mapped[ProductoModel] = relationship(
        "ProductoModel",
        back_populates="etiquetas"
    )

    etiqueta: Mapped[EtiquetaModel] = relationship(
        "EtiquetaModel",
        back_populates="productos"
    )

    def __repr__(self) -> str:
        return f"ProductoEtiquetaModel(id_producto={self.id_producto!r}, id_etiqueta={self.id_etiqueta!r}, estado={self.estado!r})"
