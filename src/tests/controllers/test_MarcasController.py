import pytest
from unittest.mock import patch
from src.controllers.MarcasController import MarcasController

@patch("src.controllers.marcas_controller.Marcas.listar_companias")
def test_listar_marcas_ok(mock_listar):
    mock_listar.return_value = [
        {"id_marca": 1, "nombre": "Nike"},
        {"id_marca": 2, "nombre": "Adidas"}
    ]

    result = MarcasController.listar_marcas()

    assert result is not False
    assert len(result) == 2
    mock_listar.assert_called_once()


@patch("src.controllers.marcas_controller.Marcas.listar_companias")
def test_listar_marcas_exception(mock_listar):
    mock_listar.side_effect = Exception("Error BD")

    result = MarcasController.listar_marcas()

    assert result is False


@patch("src.controllers.marcas_controller.Marcas.crear_marca")
def test_crear_marca_ok(mock_crear):
    mock_crear.return_value = True

    result = MarcasController.crear_marca(
        "Puma", "Marca deportiva", 1
    )

    assert result is True
    mock_crear.assert_called_once()


@patch("src.controllers.marcas_controller.Marcas.crear_marca")
def test_crear_marca_exception(mock_crear):
    mock_crear.side_effect = Exception("Error insert")

    result = MarcasController.crear_marca(
        "Puma", "Marca deportiva", 1
    )

    assert result is False


@patch("src.controllers.marcas_controller.Marcas.actualizar_marcas")
def test_actualizar_marca_ok(mock_actualizar):
    mock_actualizar.return_value = True

    result = MarcasController.actualizar_marca(
        1, "Nike", "Nueva desc", 2
    )

    assert result is True
    mock_actualizar.assert_called_once()


@patch("src.controllers.marcas_controller.Marcas.eliminar_marca")
def test_eliminar_marca_ok(mock_eliminar):
    mock_eliminar.return_value = True

    result = MarcasController.eliminar_marca(1)

    assert result is True
    mock_eliminar.assert_called_once()


