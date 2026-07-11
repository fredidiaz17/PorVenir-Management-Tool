from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv 
import os

load_dotenv()

db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Creacion de objeto Engine, necesario para interactuar con la bd usando sqlalchemy
engine = create_engine(db_url)

# Creador de sesiones para la bd
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_bd():
    db = SessionLocal() # Abrir la sesión. 
    try:
        yield db # Prestar la sesión
    finally:
        db.close() # Y finalmente, cerrar la sesión.

# Clase base declarativa. Ya tiene el objeto .metadata por defecto
class Base(declarative_base()):
    pass
