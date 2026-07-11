from __future__ import annotations
from sqlalchemy import String, Float,ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
from src.schemas.enums import UnidadMedidaEnum

class ProductoModel(Base):
    __tablename__ = "producto"
    
    id_producto: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cantidad_stock: Mapped[float] = mapped_column(Float, default=0.0)
    unidad_medida: Mapped[UnidadMedidaEnum] = mapped_column(SQLEnum(UnidadMedidaEnum), default= UnidadMedidaEnum.UNIDADES)
    precio_compra: Mapped[float] = mapped_column(Float)
    precio_venta: Mapped[float] = mapped_column(Float)
    porcentaje_iva: Mapped[float] = mapped_column(Float, default=0.0)
    
    id_marca: Mapped[int] = mapped_column(ForeignKey("marca.id_marca", on_delete="CASCADE"))

    # Relación con MarcaModel
    marcas: Mapped[MarcaModel] = relationship(
        "MarcaModel",
        back_populates="productos",
        cascade= "all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"Producto(id_producto={self.id_producto!r}, nombre={self.nombre!r})"