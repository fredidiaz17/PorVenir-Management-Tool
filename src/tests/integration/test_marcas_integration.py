import pytest
from src.controllers.MarcasController import MarcasController
from src.database.conexion import get_connection

def test_crear_y_listar_marca_integration():
    nombre = "Marca Test Integración"
    descripcion = "Marca creada en test de integración"
    id_compania = 1

    # Crear
    creada = MarcasController.crear_marca(nombre, descripcion, id_compania)
    assert creada is True

    # Listar
    marcas = MarcasController.listar_marcas()
    assert marcas is not None
    assert any(m["nombre"] == nombre for m in marcas)


def test_actualizar_marca_integration():
    marcas = MarcasController.listar_marcas()
    marca = marcas[-1]  # tomamos la última creada

    actualizado = MarcasController.actualizar_marca(
        marca["id_marca"],
        "Marca Actualizada",
        "Descripción actualizada",
        marca["id_compania"]
    )

    assert actualizado is True


def test_eliminar_marca_integration():
    marcas = MarcasController.listar_marcas()
    marca = marcas[-1]

    eliminado = MarcasController.eliminar_marca(marca["id_marca"])
    assert eliminado is True


