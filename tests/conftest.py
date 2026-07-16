# Configuraciones globales para las pruebas
import pytest 
from fastapi.testclient import TestClient # Objeto para crear solicitudes a nuestra API sin ejecutar un servidor real 
from sqlalchemy import create_engine # Motor que establecerá la conexión con la BD
from sqlalchemy.orm import sessionmaker # Creador de sesiones que se usarán para interactuar con la BD 
from sqlalchemy.pool import StaticPool # Pool de conexiones estático que mantendrá abiertas algunas conexiones a la BD

from src.main import app
from src.database.db_conn import Base, get_bd
import src.models as models

# Configuración de base de datos de pruebas (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Permite que múltiples hilos accedan a la misma conexión SQLite 
    poolclass=StaticPool, # Pool de conexiones estático que mantendrá abiertas algunas conexiones a la BD
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Sesión de pruebas local

def override_get_bd(): # Función que reemplaza la dependencia get_bd
    db = TestingSessionLocal() # Crear una nueva sesión de base de datos
    try:
        yield db # Proporcionar la sesión a la ruta que la necesita
    finally:
        db.close() # Cerrar la sesión

app.dependency_overrides[get_bd] = override_get_bd # Sobreescribe la dependencia get_bd con la sesión de pruebas

# Los fixtures son funciones reutilizables que preparan el entorno para una prueba y posteriormente lo limpian

@pytest.fixture(scope="function", autouse=True) # Se ejecuta antes de cada test
def setup_database():
    Base.metadata.create_all(bind=engine) # Crear todas las tablas
    yield # Cede control a la respectiva prueba
    Base.metadata.drop_all(bind=engine) # Elimina todas las tablas

@pytest.fixture # Fixture que crea un cliente de prueba. Necesario para interactuar con la API
def client(): 
    with TestClient(app) as c:
        yield c # Proporciona el cliente a la prueba


# Los siguientes fixtures fueron creados para evitar duplicación de codigo en los tests
# Ya que hay pruebas que requieren de una entidad ya creada (Como marca con compañia o producto con marca)

@pytest.fixture
def setup_compania(client):
    client.post("/api/v1/compania/", json={"nombre": "Test Compania"})

@pytest.fixture
def setup_marca(client, setup_compania):
    client.post("/api/v1/marca/", json={
        "nombre": "Test Marca",
        "descripcion": "A test marca",
        "id_compania": 1
    })

@pytest.fixture
def setup_producto(client, setup_marca):
    client.post("/api/v1/producto/", json={
        "nombre": "Test Producto",
        "precio_compra": 10.0,
        "precio_venta": 15.0,
        "id_marca": 1
    })
