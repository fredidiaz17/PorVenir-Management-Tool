from dotenv import load_dotenv
import os
import mysql.connector  # Importando la libreria para conectar

load_dotenv()


def get_connection():  # Funcion para conectar
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )