from src.database.db_conn import Base # Se importa la Base común
from .compania import CompaniaModel
from .marca import MarcaModel
from .producto import ProductoModel

# Opcional, pero permite controlar que expongo al exterior
__all__ = [
    "Base",
    "CompaniaModel",
    "MarcaModel",
    "ProductoModel",
]
