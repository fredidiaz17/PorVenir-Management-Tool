from enum import Enum

class UnidadMedida(str, Enum): # Str = string, Enum = enumeración
    GRAMOS = "Gramos"
    KILOGRAMOS = "Kilogramos"
    LIBRAS = "Libras"
    LITROS = "Litros"
    MILILITROS = "Mililitros"
    UNIDADES = "Unidades"
    DOCENAS = "Docenas"
    PAQUETES = "Paquetes"
