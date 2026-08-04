from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Float,ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.v1.schemas.enums import UnidadMedida

if TYPE_CHECKING:
    from src.models.marca import MarcaModel
    from src.models.producto_etiqueta import ProductoEtiquetaModel
    from src.models.detalle_pedido import DetallePedidoModel
    from src.models.oferta import OfertaModel
    from src.models.detalle_venta import DetalleVentaModel

class ProductoModel(Base):
    __tablename__ = "producto"
    
    id_producto: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cantidad_stock: Mapped[float] = mapped_column(Float, default=0.0)
    unidad_medida: Mapped[UnidadMedida] = mapped_column(SQLEnum(UnidadMedida), default= UnidadMedida.UNIDADES)
    precio_compra: Mapped[float] = mapped_column(Float)
    precio_venta: Mapped[float] = mapped_column(Float)
    porcentaje_iva: Mapped[float] = mapped_column(Float, default=0.0)
    
    id_marca: Mapped[int] = mapped_column(ForeignKey("marca.id_marca", ondelete="CASCADE"))

    # Relación con MarcaModel
    marca: Mapped[MarcaModel] = relationship(
        "MarcaModel",
        back_populates="productos"
    )

    # Relación con producto_etiqueta
    etiquetas: Mapped[list[ProductoEtiquetaModel]] = relationship(
        "ProductoEtiquetaModel",
        back_populates="producto",
        cascade="all, delete-orphan"
    )

    detalle_venta: Mapped[list[DetalleVentaModel]] = relationship(
        "DetalleVentaModel",
        back_populates="producto"
    )

    detalles_pedido: Mapped[list[DetallePedidoModel]] = relationship(
        "DetallePedidoModel",
        back_populates="producto"
    )
    
    # Relación con oferta
    ofertas : Mapped[list[OfertaModel]] = relationship(
        "OfertaModel",
        secondary="oferta_producto",
        back_populates="productos"
    )

    def __repr__(self) -> str:
        return f"""ProductoModel(id_producto={self.id_producto!r}, nombre={self.nombre!r}, id_marca={self.id_marca!r}, 
        cantidad_stock={self.cantidad_stock!r}, unidad_medida={self.unidad_medida!r}, precio_compra={self.precio_compra!r}, 
        precio_venta={self.precio_venta!r}, porcentaje_iva={self.porcentaje_iva!r})"""