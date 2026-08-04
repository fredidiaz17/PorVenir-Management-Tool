from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db_conn import Base

if TYPE_CHECKING:
    from src.models.marca import MarcaModel
    from src.models.oferta import OfertaModel
    from src.models.preventista import PreventistaModel

class CompaniaModel(Base):
    __tablename__ = "compania"
    
    id_compania: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    # Relación con MarcaModel
    marcas: Mapped[list[MarcaModel]] = relationship(
        "MarcaModel", # Nombre de la relación (entidad relacionada), no es obligatoria
        back_populates="compania", # Nombre del atributo en la entidad relacionada
        cascade="all, delete-orphan" # Cuando se elimina una compania, se eliminan todas sus marcas
    )

    preventistas: Mapped[list[PreventistaModel]] = relationship(
        "PreventistaModel",
        back_populates="compania",
        cascade="all, delete-orphan"
    )
    
    # Relación con oferta_compania
    ofertas : Mapped[list[OfertaModel]] = relationship(
        "OfertaModel",
        secondary="oferta_compania",
        back_populates="companias"
    )
    
    def __repr__(self) -> str:
        return f"Compania(id_compania={self.id_compania!r}, nombre={self.nombre!r})"

