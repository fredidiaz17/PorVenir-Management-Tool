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

    @staticmethod
    def crear_compania(nombre):
        if nombre == '':
            logger.Warning(f'Dato invalido')

        try:
            logger.info(f'Compania creada')
            return Compania.crear_compania(nombre)
        except Exception:
            logger.Error(f'Error en crear compania {nombre}')

    @staticmethod
    def actualizar_compania(nombre):
        if nombre == '':
            logger.Warning(f'Dato invalido')

        try:
            logger.info(f'Compania actualizada')
            return Compania.actualizar_compania(nombre)
        except Exception:
            logger.Error(f'Error en actualizar compania {nombre}')

    @staticmethod
    def eliminar_compania(idCompania):
        try:
            logger.info(f'Compania eliminada')
            return Compania.eliminar_compania(idCompania)
        except Exception:
            logger.Error(f'Error en eliminar compania {idCompania}')


