
from ..database.conexion import get_connection
from ..logger_config import logger


class Producto:

    @staticmethod
    def crear_producto(
            nombre, cantidad_stock, unidad_medida,
            precio_compra, precio_venta, porcentaje_iva, id_marca
        ):
        conn = None  # Inicializar conn y cursor
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Iniciando transacción
            conn.start_transaction()

            query = """
                INSERT INTO Producto 
                (nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca) 
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            """

            values = (
                nombre, cantidad_stock, unidad_medida.value,
                precio_compra, precio_venta, porcentaje_iva, id_marca
            )

            cursor.execute(query, values)

            conn.commit() # Guardar cambios
            logger.info(f"Producto '{nombre}' creado correctamente")

            return True

        except Exception:
            if conn:
                conn.rollback()  # Deshacer cambios si algo falla
            logger.error("Error en crear_producto:", exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def listar_productos():
        conn = None
        cursor = None

        try:
            conn = get_connection()  # Establecer la conexión
            cursor = conn.cursor(dictionary=True)  # Entregar valores como diccionario
            cursor.execute("SELECT * FROM Producto")
            productos = cursor.fetchall()
            logger.info(f'{len(productos)} productos obtenidos correctamente')
            return productos

        except Exception:
            logger.error('Error en listar_productos:', exc_info=True)  # exc_info da más información del error.
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def eliminar_producto(id_producto):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = "DELETE FROM producto WHERE id_producto = %s"
            values = (id_producto,)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f"Producto eliminado correctamente")
            return True

        except Exception:
            if conn:
                conn.rollback()
            logger.error("Error en eliminar_producto:", exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def actualizar_producto(
        id_producto, nombre, cantidad_stock, unidad_medida,
        precio_compra, precio_venta, porcentaje_iva, id_marca
        ):

        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                    UPDATE producto 
                    SET nombre = %s, cantidad_stock = %s, unidad_medida = %s, 
                        precio_compra = %s, precio_venta = %s, porcentaje_iva = %s, 
                        id_marca = %s 
                    WHERE id_producto = %s
                """
            values = (
                nombre, cantidad_stock, unidad_medida.value,
                precio_compra, precio_venta, porcentaje_iva, id_marca,
                id_producto
            )

            cursor.execute(query, values)
            conn.commit()

            logger.info(f"Producto actualizado correctamente")
            return True

        except Exception:
            if conn:
                conn.rollback()
            logger.error("Error en actualizar_producto:", exc_info=True)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


