from database import Base # Se importa la Base común
from src.models.compania import CompaniaModel
from src.models.marca import MarcaModel
from src.models.producto import ProductoModel

# Opcional, pero permite controlar que expongo al exterior
__all__ = [
    "Base"
    "CompaniaModel",
    "MarcaModel",
    "ProductoModel",
]
