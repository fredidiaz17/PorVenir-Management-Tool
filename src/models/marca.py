from __future__ import annotations # Con esto se evita el import circular
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base
# from src.models.compania import CompaniaModel

class MarcaModel(Base):
    __tablename__ = "marca"
    
    id_marca: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)

    # Clave foránea que representa la relación con compania model
    id_compania = mapped_column(ForeignKey("compania.id_compania", on_delete="CASCADE")) # On delete cascade: Cuando se elimina una compania, se eliminan todas sus marcas

    # Relación con compania model
    compania: Mapped[CompaniaModel] = relationship("CompaniaModel", back_populates="marcas")

    # Relación con producto model
    productos: Mapped[list[ProductoModel]] = relationship(
        "ProductoModel", 
        back_populates="marca", 
        cascade="all, delete-orphan"
    )
