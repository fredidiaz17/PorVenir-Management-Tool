from src.database.conexion import get_connection
from src.logger_config import logger

class Compania():

    @staticmethod
    def crear_compania(nombre):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            conn.start_transaction()

            query = """
                INSERT INTO Compania (nombre) VALUES (%s)          
            """
            values = (nombre)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f'Compania {nombre} creado correctamente')

            return True
        except Exception:
            if conn:
                conn.rollback()
            logger.error(f'Error en crear_producto:', exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def listar_companias():
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Compania')
            companias = cursor.fetchall()
            logger.info(f'{len(companias)} companias obtenidas correctamente')
            return companias

        except Exception:
            logger.error(f'Error en listar_companias:', exc_info=True)
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def actualizar_compania(id_compania, nombre):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            conn.start_transaction()

            query = """
                    UPDATE Compania 
                    SET nombre = %s 
                    WHERE id_compania = %s
                    """
            values = (nombre, id_compania)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f'Compania {nombre} actualizada correctamente')

            return True
        except Exception:
            if conn:
                conn.rollback()
            logger.error(f'Error en actualizar_companias:', exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def eliminar_compania(id_compania):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            conn.start_transaction()

            query = """
                    DELETE FROM Compania
                        WHERE id_compania = %s
                    """
            values = (id_compania)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f'Compania eliminada correctamente')

            return True
        except Exception:
            if conn:
                conn.rollback()
            logger.error(f'Error en eliminar_compania:', exc_info=True)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()




