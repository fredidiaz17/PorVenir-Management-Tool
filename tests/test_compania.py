def test_create_compania(client):
    # Se crea la compañia
    response = client.post("/api/v1/compania/", json={"nombre": "Test Compania"}) 

    # Se verifica que fue exitosa la creación
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_get_companias(client):
    # Al no haber conexión real con una bd, es necesario crear una instancia de compañia para poder obtenerlas
    client.post("/api/v1/compania/", json={"nombre": "Test Compania"})

    # Ahora si, se obtiene la lista de companias
    response = client.get("/api/v1/compania/")

    # Se valida que la respuesta sea exitosa y que exista al menos una compañia
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["data"]) > 0

def test_get_compania(client): # Prueba para obtener una compañia por ID
    client.post("/api/v1/compania/", json={"nombre": "Test Compania"})
    response = client.get("/api/v1/compania/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == "Test Compania"

def test_update_compania(client):
    client.post("/api/v1/compania/", json={"nombre": "Test Compania"})
    response = client.put("/api/v1/compania/1", json={"nombre": "Updated Compania"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/compania/1")
    assert get_response.json()["data"]["nombre"] == "Updated Compania"

def test_delete_compania(client):
    client.post("/api/v1/compania/", json={"nombre": "Test Compania"})
    response = client.delete("/api/v1/compania/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/compania/1")
    assert get_response.json()["status"] == "error"
