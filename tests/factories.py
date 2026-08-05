from sqlalchemy.orm import scoped_session, sessionmaker
from src.v1.schemas.enums import UnidadMedida
import factory
from factory import alchemy, SubFactory, LazyFunction
from faker import Faker
from src.models import CompaniaModel, MarcaModel, ProductoModel, EtiquetaModel, ProductoEtiquetaModel, OfertaModel, PreventistaModel, PedidoModel, DetallePedidoModel, ClienteModel, VentaModel, DetalleVentaModel, DeudaModel, Base

# factory-boy es una libreria que permite crear instancias de modelos de forma automatizada
# Es util para los test ya que permite ser mas eficaz y concreto en la realización de ellos,
# pues crearían los datos relacionales automáticamente y nos permite concentrarnos en el test concreto.


TestSession = scoped_session(sessionmaker())
fake = Faker()

class BaseFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Base # Origen del modelo. Este es el modelo base
        abstract = True
        sqlalchemy_session = TestSession
        sqlalchemy_session_persistence = "flush"
    
class CompaniaFactory(BaseFactory):
    class Meta:
        model = CompaniaModel
    
    nombre = LazyFunction(lambda: fake.text(max_nb_chars=100))

class MarcaFactory(BaseFactory):
    class Meta:
        model = MarcaModel
    
    nombre = LazyFunction(lambda: fake.text(max_nb_chars=100))
    descripcion = LazyFunction(lambda: fake.text(max_nb_chars=255))
    compania = SubFactory(CompaniaFactory)
    
class ProductoFactory(BaseFactory):
    class Meta:
        model = ProductoModel
    
    nombre = "ProductoTest"
    cantidad_stock = 100.0
    unidad_medida = UnidadMedida.UNIDADES
    precio_compra = 5.0
    precio_venta = 10.0
    porcentaje_iva = 0.19
    marca = SubFactory(MarcaFactory)

class EtiquetaFactory(BaseFactory):
    class Meta:
        model = EtiquetaModel
    
    nombre_etiqueta = LazyFunction(lambda: fake.text(max_nb_chars=50))
    descripcion_etiqueta = LazyFunction(lambda: fake.text(max_nb_chars=255))
    color_hex = LazyFunction(lambda: fake.hex_color())

class PreventistaFactory(BaseFactory):
    class Meta:
        model = PreventistaModel
    
    nombre = LazyFunction(lambda: fake.first_name())
    telefono = LazyFunction(lambda: fake.bothify(text='#########'))
    compania = SubFactory(CompaniaFactory)


class ProductoEtiquetaFactory(BaseFactory):
    class Meta:
        model = ProductoEtiquetaModel
    
    producto = SubFactory(ProductoFactory)
    etiqueta = SubFactory(EtiquetaFactory)
    estado = LazyFunction(lambda: fake.random_element(elements=["Activo", "Inactivo"]))
