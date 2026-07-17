from src.database.db_conn import Base # Se importa la Base común
from .compania import CompaniaModel
from .marca import MarcaModel
from .producto import ProductoModel
from .etiqueta import EtiquetaModel
from .producto_etiqueta import ProductoEtiquetaModel
from .oferta import OfertaModel
from .preventista import PreventistaModel
from .pedido import PedidoModel
from .detalle_pedido import DetallePedidoModel

# Opcional, pero permite controlar que expongo al exterior
__all__ = [
    "Base",
    "CompaniaModel",
    "MarcaModel",
    "ProductoModel",
    "EtiquetaModel",
    "ProductoEtiquetaModel",
    "OfertaModel",
    "PreventistaModel",
    "PedidoModel",
    "DetallePedidoModel",
]
