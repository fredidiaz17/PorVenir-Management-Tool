# Configuraciones globales para las pruebas
import pytest 
from fastapi.testclient import TestClient # Objeto para crear solicitudes a nuestra API sin ejecutar un servidor real 
from sqlalchemy import create_engine # Motor que establecerá la conexión con la BD
from sqlalchemy.orm import sessionmaker # Creador de sesiones que se usarán para interactuar con la BD 
from sqlalchemy.pool import StaticPool # Pool de conexiones estático que mantendrá abiertas algunas conexiones a la BD

from tests.factories import TestSession, BaseFactory, CompaniaFactory, MarcaFactory, ProductoFactory, EtiquetaFactory, PreventistaFactory, ProductoEtiquetaFactory
from src.main import app
from src.database.db_conn import Base, get_bd

# Configuración de base de datos de pruebas (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Permite que múltiples hilos accedan a la misma conexión SQLite 
    poolclass=StaticPool, # Pool de conexiones estático que mantendrá abiertas algunas conexiones a la BD
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Sesión de pruebas local

# Los fixtures son funciones reutilizables que preparan el entorno para una prueba y posteriormente lo limpian

@pytest.fixture(scope="session", autouse= True)
def test_bd():
    Base.metadata.create_all(bind=engine) # Crear todas las tablas
    yield # Proporcionar la sesión a la ruta que la necesita
    Base.metadata.drop_all(bind=engine) # Elimina todas las tablas

@pytest.fixture(scope="function")
def db_session():
    # Crear y limpiar la sesión de BD para cada test
    session = TestingSessionLocal() # Crear una nueva sesión de base de datos
    yield session # Proporcionar la sesión a la ruta que la necesita
    session.close() # Cerrar la sesión

@pytest.fixture(autouse=True)
def bind_factory_session(db_session):
    # Asignamos la sesión de la BD actual al registry del TestSession
    TestSession.configure(bind=db_session.get_bind())
    
    # Inyectamos directamente la instancia de la sesión
    TestSession.session_factory.config = db_session
    
    yield
    
    # Limpiamos la sesión al terminar el test
    TestSession.remove()


@pytest.fixture(autouse= True)
def override_db(db_session):
    def _get_test_db():
        try:
            yield db_session
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            pass # No la cerramos aquí porque la maneja la fixture db_session

    # Sobreescribimos la dependencia de get_bd de los routers 
    app.dependency_overrides[get_bd] = _get_test_db
    yield
    app.dependency_overrides.clear()
    

@pytest.fixture # Fixture que crea un cliente de prueba. Necesario para interactuar con la API
def client(): 
    with TestClient(app) as c:
        yield c # Proporciona el cliente a la prueba

# Fixtures de creación de datos

@pytest.fixture(scope="module")
def setup_marca():
    return MarcaFactory()

@pytest.fixture(scope="module")
def setup_producto():
    return ProductoFactory()

@pytest.fixture(scope="module")
def setup_etiqueta():
    return EtiquetaFactory()

@pytest.fixture(scope="module")
def setup_preventista():
    return PreventistaFactory()

@pytest.fixture(scope="module")
def setup_producto_etiqueta():
    return ProductoEtiquetaFactory()