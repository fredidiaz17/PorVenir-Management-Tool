from src.models.marcas import Marcas
from src.logger_config import logger

class MarcasController:

    def __init__(self, companias_controller):
        self.companias_controller = companias_controller

    @staticmethod
    def listar_marcas():
        try:
            logger.info(f'Marccas listada')
            return Marcas.listar_marcas()
        except Exception:
            logger.Error(f'Error en controlador de listar companias')
            return False

    @staticmethod
    def crear_marca(nombre, descripcion, id_compania):

        try:
            logger.info(f'Marca creada')
            return Marcas.crear_marca(nombre, descripcion, id_compania)
        except Exception:
            logger.Error(f'Error en crear marca {nombre}')
        return False

    @staticmethod
    def actualizar_marca(id_marca, nombre, descripcion, id_compania):

        try:
            logger.info(f'Marca actualizada')
            return Marcas.actualizar_marcas(id_marca, nombre, descripcion, id_compania)
        except Exception:
            logger.Error(f'Error en actualizar marca {nombre}')
        return False # Si llega hasta acá, pues hubo excepción.


    @staticmethod
    def eliminar_marca(id_marca):
        try:
            logger.info(f'Marca eliminada')
            return Marcas.eliminar_marca(id_marca)
        except Exception:
            logger.Error(f'Error en eliminar marca {id_marca}')
            return False

    # ------Metodos de Compañias-------
    @staticmethod
    def listar_companias(self):
        return self.companias_controller.listar_companias()