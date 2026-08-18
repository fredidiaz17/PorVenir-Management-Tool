# Configuraciones globales para las pruebas
import pytest 
from fastapi.testclient import TestClient # Objeto para crear solicitudes a nuestra API sin ejecutar un servidor real 
from sqlalchemy import create_engine # Motor que establecerá la conexión con la BD
from sqlalchemy.orm import sessionmaker # Creador de sesiones que se usarán para interactuar con la BD 
from sqlalchemy.pool import StaticPool # Pool de conexiones estático que mantendrá abiertas algunas conexiones a la BD

from tests.factories import TestSession, BaseFactory, CompaniaFactory, MarcaFactory, ProductoFactory, EtiquetaFactory, PreventistaFactory, ProductoEtiquetaFactory, OfertaFactory, PedidoFactory, DetallePedidoFactory, ClienteFactory, VentaFactory, DetalleVentaFactory, DeudaFactory
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


# Con tal de mantener scope modular de los fixtures de setup y de mantener el scope de las sesiones. 
# Se ha decidido hacer sesiones anidadas (nested transactions)

@pytest.fixture(scope="module")
def connection():
    # Maintain one connection for the duration of the module
    conn = engine.connect()
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def module_db_session(connection):
    # This session will be used by module-scoped setup fixtures
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback() # Roll back everything created in the module setup

@pytest.fixture(scope="module", autouse=True)
def bind_module_factory_session(module_db_session):
    TestSession.configure(bind=module_db_session.get_bind())
    TestSession.session_factory.config = module_db_session
    yield
    TestSession.remove()


@pytest.fixture(scope="function")
def db_session(connection):
    # This session runs each test inside a nested transaction (savepoint)
    transaction = connection.begin_nested()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback() # Roll back changes made during the test function


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
    def _assert_status(response, expected_status: int):
        assert response.status_code == expected_status, (
            f"\nStatus esperado: {expected_status}"
            f"\nStatus obtenido: {response.status_code}"
            f"\nRespuesta del Server (detail): {response.json().get('detail')}"
        )
        return response.json()
    with TestClient(app) as c:
        c.assert_status = _assert_status
        yield c # Proporciona el cliente a la prueba

# Fixtures de creación de datos

@pytest.fixture(scope="module")
def setup_compania():
    compania = CompaniaFactory()
    return {"compania": compania}

@pytest.fixture(scope="module")
def setup_marca():
    compania = CompaniaFactory()
    marca = MarcaFactory(compania = compania)
    return {"compania": compania, "marca": marca}

@pytest.fixture(scope="module")
def setup_producto():
    marca = MarcaFactory()
    producto = ProductoFactory(marca=marca)
    return {"marca": marca, "producto": producto}

@pytest.fixture(scope="module")
def setup_etiqueta():
    etiqueta = EtiquetaFactory()
    return {"etiqueta": etiqueta}

@pytest.fixture(scope="module")
def setup_preventista():
    compania = CompaniaFactory()
    preventista = PreventistaFactory(compania=compania)
    return {"compania": compania, "preventista": preventista}

@pytest.fixture(scope="module")
def setup_producto_etiqueta():
    producto = ProductoFactory()
    etiqueta_1 = EtiquetaFactory()
    producto_etiqueta = ProductoEtiquetaFactory(producto=producto, etiqueta=etiqueta_1)
    etiqueta_2= EtiquetaFactory()
    return {"producto": producto, "etiqueta_1": etiqueta_1, "etiqueta_2": etiqueta_2, "producto_etiqueta": producto_etiqueta}

@pytest.fixture(scope="module")
def setup_oferta():
    oferta = OfertaFactory()
    compania = CompaniaFactory()
    marca = MarcaFactory(compania=compania)
    producto = ProductoFactory(marca = marca)
    etiqueta = EtiquetaFactory()
    return {"oferta": oferta, "marca": marca, "compania": compania, "producto": producto, "etiqueta": etiqueta}

@pytest.fixture(scope="module")
def setup_pedido():
    preventista = PreventistaFactory()
    pedido = PedidoFactory(preventista=preventista)
    producto = ProductoFactory()
    detalle_pedido = DetallePedidoFactory(pedido=pedido, producto=producto)
    return {"preventista": preventista, "pedido": pedido, "detalle_pedido": detalle_pedido, "producto": producto}

@pytest.fixture(scope="module")
def setup_cliente():
    cliente = ClienteFactory()
    return {"cliente": cliente}

@pytest.fixture(scope="module")
def setup_venta():
    cliente = ClienteFactory()
    venta = VentaFactory(cliente=cliente)
    producto = ProductoFactory()
    detalle_venta = DetalleVentaFactory(venta=venta, producto=producto)
    return {"cliente": cliente, "venta": venta, "producto": producto, "detalle_venta": detalle_venta}

@pytest.fixture(scope="module")
def setup_deuda():
    cliente = ClienteFactory()
    deuda = DeudaFactory(cliente=cliente)
    return {"cliente": cliente, "deuda": deuda}