from enum import Enum

# Enum usado por producto 

class UnidadMedida(str, Enum): 
    GRAMOS = "Gramos"
    KILOGRAMOS = "Kilogramos"
    LIBRAS = "Libras"
    LITROS = "Litros"
    MILILITROS = "Mililitros"
    UNIDADES = "Unidades"
    DOCENAS = "Docenas"
    PAQUETES = "Paquetes"

# Enums usado por oferta

class TipoOferta(str, Enum):
    DESCUENTO = "Descuento"
    COMBO = "Combo"
    OTRO = "Otro"

class EstadoOferta(str, Enum):
    ACTIVA = "Activa"
    INACTIVA = "Inactiva"
    FINALIZADA = "Finalizada"


# Enums usado por pedido

class EstadoPedido(str, Enum):
    PENDIENTE = "Pendiente"
    EN_CAMINO = "En camino"
    RECIBIDO = "Recibido"
    RECHAZADO = "Rechazado"
    CANCELADO = "Cancelado"
