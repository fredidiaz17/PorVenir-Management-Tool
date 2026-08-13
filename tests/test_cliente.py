def test_create_cliente(client, setup_cliente):
    resp = client.post("/api/v1/cliente/", json={
        "nombre": "Cliente Nuevo",
        "telefono": "123456789"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_clientes(client, setup_cliente):
    resp = client.get("/api/v1/cliente/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert len(resp.json()["data"]) > 0

def test_get_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.get(f"/api/v1/cliente/{c.id_cliente}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert resp.json()["data"]["nombre"] == c.nombre

def test_update_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.put(f"/api/v1/cliente/{c.id_cliente}", json={
        "nombre": "Cliente Modificado",
        "telefono": "987654321"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_patch_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.patch(f"/api/v1/cliente/{c.id_cliente}", json={
        "nombre": "Cliente Parcial"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_delete_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.delete(f"/api/v1/cliente/{c.id_cliente}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    resp = client.get(f"/api/v1/cliente/{c.id_cliente}")
    assert resp.status_code == 404
