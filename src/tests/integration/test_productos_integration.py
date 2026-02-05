from src.controllers.ProductosController import ProductoController

# Todo: Mejorar el test, está bien a un nivel basico, pero falta pulido (Quizá demasiado)

def test_crear_listar_productos():
    # Producto 1
    nombre1= "Producto_test1"
    cantidad_stock1= 4
    unidad_medida1= "PAQUETES"
    precio_compra1 = 3000
    precio_venta1= 3300
    porcentaje_iva1= 3
    id_marca1 = 1

    # Producto 2
    nombre2 = "Producto_test2"
    cantidad_stock2 = 10
    unidad_medida2 = "UNIDADES"
    precio_compra2 = 1200
    precio_venta2 = 1300
    porcentaje_iva2 = 2
    id_marca2 = 1

    # Producto 3, debe dar error
    nombre3 = "Producto_test1"
    cantidad_stock3= 400
    unidad_medida3 = "GRR"
    precio_compra3 = 200
    precio_venta3= 300
    porcentaje_iva3 = 0
    id_marca3 = 1

    #CREAR
    producto1 = ProductoController.crear_producto(
        nombre1, cantidad_stock1, unidad_medida1,
        precio_compra1, precio_venta1, porcentaje_iva1, id_marca1
    )

    producto2 = ProductoController.crear_producto(
        nombre2, cantidad_stock2, unidad_medida2,
        precio_compra2, precio_venta2, porcentaje_iva2, id_marca2
    )

    producto3 = ProductoController.crear_producto(
        nombre3, cantidad_stock3, unidad_medida3,
        precio_compra3, precio_venta3, porcentaje_iva3, id_marca3
    )

    assert producto1 is True and producto2 is True and producto3 is False

    #Listar

    productos = ProductoController.listar_productos()

    assert isinstance(productos, list)
    assert len(productos) >= 2

def buscar_por_nombre(nombre):
    productos = ProductoController.listar_productos()

    for p in productos:
        if p["nombre"] == nombre:

            return p["id_producto"]

def test_actualizar_producto():

    id1 = buscar_por_nombre("Producto_test1")
    id2 = buscar_por_nombre("Producto_test2")

    # Cambios en producto 2
    nombre2= "Producto_test2_actualizado"
    cantidad_stock2 = 4
    unidad_medida2 = "KILOGRAMOS"
    precio_compra2 = 15000
    precio_venta2 = 16500
    porcentaje_iva2 =  0
    id_marca2 = 1

    # Cambios en producto 1, debe dar error

    nombre1 = "Producto_test1_actualizado"
    cantidad_stock1 = 221
    unidad_medida1 = "pqts"
    precio_compra1 = 0
    precio_venta1 = 0
    porcentaje_iva1 = 0
    id_marca1 = 0

    producto1_actualizado = ProductoController.actualizar_producto(
        id1,nombre1, cantidad_stock1, unidad_medida1,
        precio_compra1, precio_venta1, porcentaje_iva1, id_marca1
    )

    producto2_actualizado = ProductoController.actualizar_producto(
        id2,nombre2, cantidad_stock2, unidad_medida2,
        precio_compra2, precio_venta2, porcentaje_iva2, id_marca2
    )

    assert producto1_actualizado is False and producto2_actualizado is True

def test_eliminar_productos():
    id = buscar_por_nombre("Producto_test2_actualizado")

    eliminado = ProductoController.eliminar_producto(id)

    assert eliminado is True

    productos = ProductoController.listar_productos()
    assert isinstance(productos, list)
    assert len(productos) >= 2

    for p in productos: assert p["id_producto"] != id
