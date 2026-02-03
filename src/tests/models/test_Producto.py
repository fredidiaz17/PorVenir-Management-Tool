from src.models.producto import Producto
from src.models.enums import productos_enum

def test_crear_producto_ok():
    producto = None
    unidad_medida = None
    try:
        unidad_medida = productos_enum["UNIDADES"] #No se puede pasar directamente la conversión del enum, ya que no hace la conversión
    except KeyError:
            producto = False
    if not producto:
        producto = Producto.crear_producto(
            nombre= "producto_prueba",
            cantidad_stock=13.00,
            unidad_medida= unidad_medida,
            precio_compra= 1400.00,
            precio_venta= 1500.00,
            porcentaje_iva= 0.00,
            id_marca= 1
        )
    assert producto is True

def test_producto_por_id(nombre):
    productos = Producto.listar_productos()

    for producto in productos:
        if producto["nombre"] == nombre:
            return producto["id_producto"]

    return None

def test_listar_productos_ok():
    productos = Producto.listar_productos()

    assert productos is not None
    assert isinstance(productos, list)
    assert len(productos) > 0

def test_actualizar_producto():
    producto_id = test_producto_por_id("producto_prueba")
    assert producto_id is not None

    actualizado = None
    unidad_medida = None

    try:
        unidad_medida = productos_enum["PAQUETES"]
    except KeyError:
        actualizado = False

    if not actualizado:
        actualizado = Producto.actualizar_producto(
            id_producto= producto_id,
            nombre="producto_prueba_cambiado",
            cantidad_stock=7,
            unidad_medida=unidad_medida,
            precio_compra=2000,
            precio_venta=2200,
            porcentaje_iva=2,
            id_marca=1
        )

    assert actualizado is True

    productos = Producto.listar_productos()
    nombre = [p["nombre"] for p in productos]
    assert "producto_prueba_cambiado" in nombre



def test_eliminar_producto():
    producto_id = test_producto_por_id("producto_prueba_cambiado")
    assert producto_id is not None

    eliminado = Producto.eliminar_producto(producto_id)

    assert eliminado is True

def test_eliminar_producto_ok():
    productos = Producto.listar_productos()
    nombre = [p["nombre"] for p in productos]

    assert "producto_prueba_cambiado" not in nombre