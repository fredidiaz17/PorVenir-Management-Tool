from src.models.marcas import Marcas
from src.logger_config import logger

class MarcasController:

    @staticmethod
    def listar_marcas():
        try:
            logger.info(f'Marccas listada')
            return Marcas.listar_companias()
        except Exception:
            logger.Error(f'Error en controlador de listar companias')
            return False

    @staticmethod
    def crear_marcas(nombre, descripcion, id_compania):

        try:
            logger.info(f'Marca creada')
            return Marcas.crear_marca([nombre, descripcion, id_compania])
        except Exception:
            logger.Error(f'Error en crear marca {nombre}')
        return False

    @staticmethod
    def actualizar_marcas(id_marca, nombre, descripcion, id_compania):

        try:
            logger.info(f'Marca actualizada')
            return Marcas.actualizar_marcas([id_marca, nombre, descripcion, id_compania])
        except Exception:
            logger.Error(f'Error en actualizar marca {nombre}')
        return False # Si llega hasta acá, pues hubo excepción.


    @staticmethod
    def eliminar_marca(id_marca):
        try:
            logger.info(f'Marca eliminada')
            return Marcas.eliminar_marca([id_marca])
        except Exception:
            logger.Error(f'Error en eliminar marca {id_marca}')
            return False