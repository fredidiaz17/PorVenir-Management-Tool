def test_create_oferta(client, setup_oferta):
    resp = client.post("/api/v1/oferta/", json={
        "nombre": "Oferta Especial",
        "descripcion": "Descripción de la oferta especial",
        "tipo_oferta": "Descuento",
        "valor_descuento": 15.0,
        "cantidad_minima": 2,
        "producto_regalo": 0,
        "fecha_inicio": "2026-08-05T12:00:00",
        "fecha_fin": "2026-08-15T12:00:00",
        "estado": "Activa"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_get_ofertas(client, setup_oferta):
    resp = client.post("/api/v1/oferta/", json={
        "nombre": "Oferta Especial",
        "descripcion": "Descripción de la oferta especial",
        "tipo_oferta": "Descuento",
        "valor_descuento": 15.0,
        "cantidad_minima": 2,
        "producto_regalo": 0,
        "fecha_inicio": "2026-08-05T12:00:00",
        "fecha_fin": "2026-08-15T12:00:00",
        "estado": "Activa"
    })
    nombre_oferta = setup_oferta["oferta"].nombre

    resp = client.get("/api/v1/oferta/")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert len(data["data"]) >= 2
    assert any(o["nombre"] == nombre_oferta for o in data["data"])

def test_get_oferta(client, setup_oferta):
    resp = client.get(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == setup_oferta["oferta"].nombre

def test_update_oferta(client, setup_oferta):
    resp = client.put(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}", json={
        "nombre": "Oferta Modificada",
        "descripcion": "Nueva descripción",
        "tipo_oferta": "Combo",
        "valor_descuento": 20.0,
        "cantidad_minima": 3,
        "producto_regalo": 1,
        "fecha_inicio": "2026-08-05T12:00:00",
        "fecha_fin": "2026-08-20T12:00:00",
        "estado": "Activa"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_patch_oferta(client, setup_oferta):
    resp = client.patch(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}", json={
        "nombre": "Oferta Parcial"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_delete_oferta(client, setup_oferta):
    resp = client.delete(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    resp = client.get(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}")
    client.assert_status(resp, 404)


def test_vinculacion_desvinculacion_producto(client, setup_oferta):
    o = setup_oferta["oferta"]
    p = setup_oferta["producto"]
    # Vincular
    resp = client.post(f"/api/v1/oferta/vinculacion/Producto/{p.id_producto}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    """# Ver vinculación
    resp = client.get(f"/api/v1/oferta/{o.id_oferta}/productos")
    data = client.assert_status(resp, 200)
    assert any(prod["id_producto"] == p.id_producto for prod in resp.json()["data"])"""

    # Desvincular
    resp = client.delete(f"/api/v1/oferta/desvinculacion/Producto/{p.id_producto}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"


def test_vinculacion_desvinculacion_compania(client, setup_oferta):
    o = setup_oferta["oferta"]
    c = setup_oferta["compania"]
    # Vincular
    resp = client.post(f"/api/v1/oferta/vinculacion/Compania/{c.id_compania}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    """
    # Ver vinculación
    resp = client.get(f"/api/v1/oferta/{o.id_oferta}/companias")
    data = client.assert_status(resp, 200)
    assert any(comp["id_compania"] == c.id_compania for comp in resp.json()["data"])
    """
    # Desvincular
    resp = client.delete(f"/api/v1/oferta/desvinculacion/Compania/{c.id_compania}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"


def test_vinculacion_desvinculacion_etiqueta(client, setup_oferta):
    o = setup_oferta["oferta"]
    e = setup_oferta["etiqueta"]
    # Vincular
    resp = client.post(f"/api/v1/oferta/vinculacion/Etiqueta/{e.id_etiqueta}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    """
    # Ver vinculación
    resp = client.get(f"/api/v1/oferta/{o.id_oferta}/etiquetas")
    data = client.assert_status(resp, 200)
    assert any(etiq["id_etiqueta"] == e.id_etiqueta for etiq in resp.json()["data"])
    """
    # Desvincular
    resp = client.delete(f"/api/v1/oferta/desvinculacion/Etiqueta/{e.id_etiqueta}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"


def test_vinculacion_desvinculacion_marca(client, setup_oferta):
    o = setup_oferta["oferta"]
    m = setup_oferta["marca"]
    # Vincular
    resp = client.post(f"/api/v1/oferta/vinculacion/Marca/{m.id_marca}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    """
    # Ver vinculación
    resp = client.get(f"/api/v1/oferta/{o.id_oferta}/marcas")
    data = client.assert_status(resp, 200)
    assert any(mar["id_marca"] == m.id_marca for mar in resp.json()["data"])
    """
    # Desvincular
    resp = client.delete(f"/api/v1/oferta/desvinculacion/Marca/{m.id_marca}/Oferta/{o.id_oferta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"


