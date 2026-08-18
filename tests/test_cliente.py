def test_create_cliente(client, setup_cliente):
    resp = client.post("/api/v1/cliente/", json={
        "nombre": "Cliente Nuevo",
        "telefono": "123456789"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_get_clientes(client, setup_cliente):
    resp = client.get("/api/v1/cliente/")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert len(data["data"]) > 0

def test_get_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.get(f"/api/v1/cliente/{c.id_cliente}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == c.nombre

def test_update_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.put(f"/api/v1/cliente/{c.id_cliente}", json={
        "nombre": "Cliente Modificado",
        "telefono": "987654321"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_patch_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.patch(f"/api/v1/cliente/{c.id_cliente}", json={
        "nombre": "Cliente Parcial"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_delete_cliente(client, setup_cliente):
    c = setup_cliente["cliente"]
    resp = client.delete(f"/api/v1/cliente/{c.id_cliente}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    resp = client.get(f"/api/v1/cliente/{c.id_cliente}")
    data = client.assert_status(resp, 404)
