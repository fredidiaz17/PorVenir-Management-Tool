import pytest
from src.models.marcas import Marcas


def test_crear_marca_ok():
    resultado = Marcas.crear_marca(
        nombre="Marca Test",
        descripcion="Marca creada desde test",
        id_compania=1
    )

    assert resultado is True

def obtener_id_marca_por_nombre(nombre):
    marcas = Marcas.listar_marcas()
    for marca in marcas:
        if marca["nombre"] == nombre:
            return marca["id_marca"]
    return None

def test_listar_marcas():
    marcas = Marcas.listar_marcas()

    assert marcas is not None
    assert isinstance(marcas, list)
    assert len(marcas) > 0

def test_actualizar_marca():
    id_marca = obtener_id_marca_por_nombre("Marca Test")
    assert id_marca is not None

    resultado = Marcas.actualizar_marcas(
        id_marca=id_marca,
        nombre="Marca Test Actualizada",
        descripcion="Descripcion actualizada",
        id_compania=2
    )

    assert resultado is True

def test_eliminar_marca():
    id_marca = obtener_id_marca_por_nombre("Marca Test Actualizada")
    assert id_marca is not None

    resultado = Marcas.eliminar_marca(id_marca)

    assert resultado is True

def test_marca_eliminada_no_existe():
    marcas = Marcas.listar_marcas()
    nombres = [m["nombre"] for m in marcas]

    assert "Marca Test Actualizada" not in nombres
