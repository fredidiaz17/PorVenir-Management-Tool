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
                INSERT INTO producto (nombre, cantidad_stock, unidad_medida,
            precio_compra, precio_venta, porcentaje_iva, id_marca)
            VALUES (%s, %s, %s, %s, %s, %s,%s)
            """
            values = (
                nombre, cantidad_stock, unidad_medida,
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

        try:
            conn = get_connection()  # Establecer la conexión
            cursor = conn.cursor(dictionary=True)  # Entregar valores como diccionario
            cursor.execute("SELECT * FROM producto")
            productos = cursor.fetchall()
            logger.info(f'{len(productos)} productos obtenidos correctamente')
            return productos

        except Exception as e:
            logger.error('Error en listar_productos:', exc_info=True)  # exc_info da mas información del error.
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def eliminar_producto(id_producto):
        conn = get_connection()
        cursor = conn.cursor

        cursor.execute("DELETE FROM producto WHERE id = %s", (id_producto,))

