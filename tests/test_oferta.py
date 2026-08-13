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
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

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
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert len(resp.json()["data"]) >= 2
    assert any(o["nombre"] == nombre_oferta for o in resp.json()["data"])

def test_get_oferta(client, setup_oferta):
    resp = client.get(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert resp.json()["data"]["nombre"] == setup_oferta["oferta"].nombre

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
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_patch_oferta(client, setup_oferta):
    resp = client.patch(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}", json={
        "nombre": "Oferta Parcial"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_delete_oferta(client, setup_oferta):
    resp = client.delete(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    resp = client.get(f"/api/v1/oferta/{setup_oferta["oferta"].id_oferta}")
    assert resp.status_code == 404

