from src.logger_config import logger
from src.models.producto import Producto
from src.models.enums import productos_enum

class ProductoController:
    # Todo: Anexar validación de datos a nivel controlador.
    def __init__(self, marcas_controller = None):
        self.marcas_controller = marcas_controller
    
    # CRUD producto
    @staticmethod
    def crear_producto(
            nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca
    ):
        # Validando unidad_medida
        try:
            unidad_medida = productos_enum[unidad_medida]
        except KeyError:
            logger.error(f'Valor del enum erroneo: {unidad_medida}')
            return False

        #Creando producto
        try:
            logger.info(f'Creando producto: {nombre}')
            return Producto.crear_producto(nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca)
        except Exception:
            logger.error(f'Error al crear producto: {nombre}')
        return False

    @staticmethod
    def listar_productos():
        try:
            logger.info(f'Listando productos')
            return Producto.listar_productos()
        except Exception:
            logger.error(f'Error al listar productos')
        return False

    @staticmethod
    def actualizar_producto(
            id_producto, nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca
    ):

        # Validando unidad_medida
        try:
            unidad_medida = productos_enum[unidad_medida]
        except KeyError:
            logger.error(f'Valor del enum erroneo: {unidad_medida}')
            return False


        try:
            logger.info(f'Actualizando producto: {nombre}')
            return Producto.actualizar_producto(
                id_producto,nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca
            )
        except Exception:
            logger.error(f'Error al actualizar producto: {nombre}')
        return False

    @staticmethod
    def eliminar_producto(id_producto):
        try:
            logger.info(f'Eliminando producto: #{id_producto}')
            return Producto.eliminar_producto(id_producto)
        except Exception:
            logger.error(f'Error al eliminar producto: #{id_producto}')
        return False

    # Marcas
    @staticmethod
    def listar_marcas(self):
        return self.marcas_controller.listar_marcas()
