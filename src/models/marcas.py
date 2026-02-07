from src.database.conexion import get_connection
from src.logger_config import logger

class Marcas:

    @staticmethod
    def crear_marca(nombre, descripcion, id_compania):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            conn.start_transaction()

            query = """
                INSERT INTO marca (nombre, descripcion, id_compania) VALUES (%s, %s, %s)          
            """
            values = nombre, descripcion, id_compania
            cursor.execute(query, values)
            conn.commit()
            logger.info(f'Marca {nombre} creada correctamente')

            return True
        except Exception:
            if conn:
                conn.rollback()
            logger.error(f'Error en crear_marca:', exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def listar_marcas():
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                           SELECT m.*, c.nombre as compania
                           FROM marca as m 
                               JOIN compania as c 
                               on m.id_compania = c.id_compania
                           """)
            marcas = cursor.fetchall()
            logger.info(f'{len(marcas)} marcas obtenidas correctamente')
            return marcas

        except Exception:
            logger.error(f'Error en listar_marcas:', exc_info=True)
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def actualizar_marcas(id_marca, nombre, descripcion, id_compania):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            conn.start_transaction()

            query = """
                    UPDATE marca 
                    SET nombre = %s,
                        descripcion = %s,
                        id_compania = %s
                    WHERE id_marca = %s
                    """
            values = (nombre, descripcion, id_compania, id_marca)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f'Marca {nombre} actualizada correctamente')

            return True
        except Exception:
            if conn:
                conn.rollback()
            logger.error(f'Error en actualizar_marcas:', exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def eliminar_marca(id_marca,):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            conn.start_transaction()

            query = """
                    DELETE FROM marca
                        WHERE id_marca = %s
                    """
            values = (id_marca)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f'Marca eliminada correctamente')

            return True
        except Exception:
            if conn:
                conn.rollback()
            logger.error(f'Error en eliminar_marca:', exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
