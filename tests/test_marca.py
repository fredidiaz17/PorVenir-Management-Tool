def test_create_marca(client, setup_compania):
    response = client.post("/api/v1/marca/", json={
        "nombre": "Test Marca",
        "descripcion": "A test marca",
        "id_compania": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_get_marcas(client, setup_marca):
    response = client.get("/api/v1/marca/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["data"]) > 0

def test_get_marca(client, setup_marca):
    response = client.get("/api/v1/marca/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == "Test Marca"

def test_update_marca(client, setup_marca):
    response = client.put("/api/v1/marca/1", json={
        "nombre": "Updated Marca",
        "descripcion": "Updated description",
        "id_compania": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/marca/1")
    assert get_response.json()["data"]["nombre"] == "Updated Marca"

def test_update_marca_parcial(client, setup_marca):
    response = client.patch("/api/v1/marca/1", json={
        "nombre": "Patched Marca"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/marca/1")
    assert get_response.json()["data"]["nombre"] == "Patched Marca"
    assert get_response.json()["data"]["descripcion"] == "A test marca"

def test_delete_marca(client, setup_marca):
    response = client.delete("/api/v1/marca/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/marca/1")
    assert get_response.json()["status"] == "error"
