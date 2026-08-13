

def test_create_marca(client, setup_marca): # Se usa el fixture para crear una marca y automaticamente una compania asociada a ella 
    id_compania = setup_marca["compania"].id_compania # Se accede a la compania subyacente y se obtiene su id
    response = client.post("/api/v1/marca/", json={
        "nombre": "Test Marca",
        "descripcion": "A test marca",
        "id_compania": id_compania 
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_get_marcas(client, setup_marca):
    # Creamos otra marca
    id_compania = setup_marca["compania"].id_compania 
    client.post("/api/v1/marca/", json={
        "nombre": "Test Marca",
        "descripcion": "A test marca",
        "id_compania": id_compania 
    })

    
    response = client.get("/api/v1/marca/")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert len(data["data"]) >= 2


def test_get_marca(client, setup_marca):
    id_marca = setup_marca["marca"].id_marca 
    nombre_marca = setup_marca["marca"].nombre
    
    response = client.get(f"/api/v1/marca/{id_marca}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == nombre_marca

def test_update_marca(client, setup_marca):
    marca_id = setup_marca["marca"].id_marca
    compania_id = setup_marca["compania"].id_compania

    response = client.put(f"/api/v1/marca/{marca_id}", json={
        "nombre": "Updated Marca",
        "descripcion": "Updated description",
        "id_compania": compania_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get(f"/api/v1/marca/{marca_id}")
    assert get_response.json()["data"]["nombre"] == "Updated Marca"

def test_update_marca_parcial(client, setup_marca):
    marca_id = setup_marca["marca"].id_marca
    response = client.patch(f"/api/v1/marca/{marca_id}", json={
        "nombre": "Patched Marca"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get(f"/api/v1/marca/{marca_id}")
    assert get_response.json()["data"]["nombre"] == "Patched Marca"

def test_delete_marca(client, setup_marca):
    marca_id = setup_marca["marca"].id_marca
    response = client.delete(f"/api/v1/marca/{marca_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get(f"/api/v1/marca/{marca_id}")
    assert get_response.status_code == 404
