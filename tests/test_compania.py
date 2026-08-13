def test_create_compania(client, setup_compania):
    # Se crea la compañia
    response = client.post("/api/v1/compania/", json={"nombre": "Test Compania"}) 

    # Se verifica que fue exitosa la creación
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_get_companias(client, setup_compania):
    # Ahora si, se obtiene la lista de companias
    response = client.get("/api/v1/compania/")

    # Se valida que la respuesta sea exitosa y que exista al menos una compañia
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["data"]) > 0

def test_get_compania(client, setup_compania): # Prueba para obtener una compañia por ID
    id_compania = setup_compania["compania"].id_compania
    response = client.get(f"/api/v1/compania/{id_compania}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_update_compania(client, setup_compania):
    id_compania = setup_compania["compania"].id_compania
    response = client.put(f"/api/v1/compania/{id_compania}", json={"nombre": "Updated Compania"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/compania/1")
    assert get_response.json()["data"]["nombre"] == "Updated Compania"

def test_delete_compania(client, setup_compania):
    id_compania = setup_compania["compania"].id_compania
    response = client.delete(f"/api/v1/compania/{id_compania}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get("/api/v1/compania/1")
    assert get_response.status_code == 404
