from src.models.compania import Compania
from src.logger_config import logger

class CompaniasController:

    @staticmethod
    def listar_companias():
        try:
            logger.info(f'Companias listada')
            return Compania.listar_companias()
        except Exception:
            logger.Error(f'Error en controlador de listar companias')
            return False

    @staticmethod
    def crear_compania(nombre):

        try:
            logger.info(f'Compania creada')
            return Compania.crear_compania([nombre])
        except Exception:
            logger.Error(f'Error en crear compania {nombre}')
        return False

    @staticmethod
    def actualizar_compania(id, nombre):

        try:
            logger.info(f'Compania actualizada')
            return Compania.actualizar_compania([id, nombre])
        except Exception:
            logger.Error(f'Error en actualizar compania {nombre}')
        return False # Si llega hasta acá, pues hubo excepción.


    @staticmethod
    def eliminar_compania(idCompania):
        try:
            logger.info(f'Compania eliminada')
            return Compania.eliminar_compania([idCompania])
        except Exception:
            logger.Error(f'Error en eliminar compania {idCompania}')
            return False

