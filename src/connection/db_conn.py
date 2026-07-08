from sqlalchemy import create_engine
from dotenv import load_dotenv 
import os

load_dotenv()

db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Creacion de objeto Engine, necesario para interactuar con la bd usando sqlalchemy
engine = create_engine(f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}", echo=True)

