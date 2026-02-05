from unittest import result
from unittest.mock import patch

from src.controllers.ProductosController import ProductoController
from src.models.enums import productos_enum # tocó
# Todo: Crear test de validación de datos una vez "creados los validadores"
# En los tests del controlador, se mockea el modelo.

# Listar
@patch("src.controllers.ProductosController.Producto.listar_productos")
def test_listar_productos_ok(mock_listar):
    mock_listar.return_value = [
        {"id_producto": 1, "Nombre_producto": "Shampoo", "id_marca": 3},
        {"id_producto": 2, "Nombre_producto": "Bebida dietetica", "id_marca": 2}
    ]

    result = ProductoController.listar_productos()

    assert isinstance(result,list) #Verificar que retornó una lista
    assert len(result) == 2 # Verificar que el tamaño de la lista retornada sea la esperada
    mock_listar.assert_called_once()

@patch("src.controllers.ProductosController.Producto.listar_productos")
def test_listar_productos_exception(mock_listar):
    mock_listar.side_effect = Exception("Error en la BD")
    result = ProductoController.listar_productos()

    assert result is False # Verificar que se produjo la excepción
    mock_listar.assert_called_once() # Verificar que se llamó

# Crear
@patch("src.controllers.ProductosController.Producto.crear_producto")
def test_crear_producto_ok(mock_crear):
    mock_crear.return_value = True
    nombre = "Shampoo"
    cantidad_stock = 2
    unidad_medida = "MILILITROS"
    precio_compra= 3000
    precio_venta= 3300
    porcentaje_iva= 0
    id_marca = 1

    result = ProductoController.crear_producto(
        nombre, cantidad_stock, unidad_medida,
        precio_compra, precio_venta, porcentaje_iva, id_marca
    )

    # El mock espera recibir lo que el controlador habría enviado al modelo,
    # por lo que es necesario hacer conversión de enum
    unidad_medida = productos_enum[unidad_medida]

    assert result is True
    mock_crear.assert_called_once_with(
        nombre, cantidad_stock, unidad_medida,
        precio_compra, precio_venta, porcentaje_iva, id_marca
    )


@patch("src.controllers.ProductosController.Producto.crear_producto")
def test_crear_producto_exception(mock_crear):
    mock_crear.side_effect = Exception("Error en la BD")

    nombre = "Shampoo"
    cantidad_stock = 2
    unidad_medida = "MILILITROS"
    precio_compra = 3000
    precio_venta = 3300
    porcentaje_iva = 0
    id_marca = 1

    result = ProductoController.crear_producto(
        nombre, cantidad_stock, unidad_medida,
        precio_compra, precio_venta, porcentaje_iva, id_marca
    )

    assert result is False
    mock_crear.assert_called_once()


# Actualizar
@patch("src.controllers.ProductosController.Producto.actualizar_producto")
def test_actualizar_producto_ok(mock_editar):
    mock_editar.return_value = True

    id_producto = 1
    nombre = "Shampoo"
    cantidad_stock = 2
    unidad_medida = "MILILITROS"
    precio_compra = 2900
    precio_venta = 3000
    porcentaje_iva = 0
    id_marca = 1

    result = ProductoController.actualizar_producto(
        id_producto, nombre, cantidad_stock, unidad_medida,
        precio_compra, precio_venta, porcentaje_iva, id_marca
    )

    assert result is True
    unidad_medida = productos_enum[unidad_medida]
    mock_editar.assert_called_once_with(
        id_producto, nombre, cantidad_stock, unidad_medida,
        precio_compra, precio_venta, porcentaje_iva, id_marca
    )

@patch("src.controllers.ProductosController.Producto.actualizar_producto")
def test_actualizar_producto_exception(mock_editar):

    mock_editar.side_effect = Exception("Error en la BD")

    id_producto = 1
    nombre = "Shampoo"
    cantidad_stock = 2
    unidad_medida = "MILILITROS"
    precio_compra = 2900
    precio_venta = 3000
    porcentaje_iva = 0
    id_marca = 1

    result = ProductoController.actualizar_producto(
        id_producto, nombre, cantidad_stock,
        unidad_medida, precio_compra, precio_venta,
        porcentaje_iva, id_marca
    )

    assert result is False
    mock_editar.assert_called_once()

# Eliminar
@patch("src.controllers.ProductosController.Producto.eliminar_producto")
def test_eliminar_producto_ok(mock_eliminar):
    mock_eliminar.return_value = True

    result = ProductoController.eliminar_producto(1)

    assert result is True
    mock_eliminar.assert_called_once()

@patch("src.controllers.ProductosController.Producto.eliminar_producto")
def test_eliminar_producto_exception(mock_eliminar):
    mock_eliminar.side_effect = Exception("Error en la BD")

    result = ProductoController.eliminar_producto(1)

    assert result is False
    mock_eliminar.assert_called_once()