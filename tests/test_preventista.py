def test_create_preventista(client, setup_preventista):
    # Create a preventista using the existing compania fixture
    resp = client.post("/api/v1/preventista/", json={
        "nombre": "TestPreventista",
        "telefono": "123456789",
        "id_compania": setup_preventista.compania.id_compania
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_preventistas(client, setup_preventista):
    # List preventistas
    resp = client.post("/api/v1/preventista/", json={
        "nombre": "TestPreventista",
        "telefono": "123456789",
        "id_compania": setup_preventista.compania.id_compania
    })
    resp = client.get("/api/v1/preventista/")
    assert resp.status_code == 200
    lst = resp.json()["data"]
    assert len(lst) >= 2
    assert any(p["nombre"] == "TestPreventista" for p in lst)

def test_get_preventista_id(client, setup_preventista):
    # Get by ID
    preventista_id = setup_preventista.id_preventista
    resp = client.get(f"/api/v1/preventista/{preventista_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["nombre"] == setup_preventista.nombre

def test_update_preventista(client, setup_preventista):
    preventista_id = setup_preventista.id_preventista
    # Update (PUT)
    resp = client.put(f"/api/v1/preventista/{preventista_id}", json={
        "nombre": "UpdatedPreventista",
        "telefono": "987654321",
        "id_compania": setup_preventista.compania.id_compania
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    resp = client.get(f"/api/v1/preventista/{preventista_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["nombre"] == "UpdatedPreventista"

def test_patch_preventista(client, setup_preventista):
    preventista_id = setup_preventista.id_preventista
    
    resp = client.patch(f"/api/v1/preventista/{preventista_id}", json={
        "telefono": "987654321",
    })

    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    resp = client.get(f"/api/v1/preventista/{preventista_id}") 
    assert resp.json()["data"]["telefono"] == "987654321"
    
    # Partial update (PATCH)
    resp = client.patch(f"/api/v1/preventista/{preventista_id}", json={"telefono": "555555555"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_delete_preventista(client, setup_preventista):
    preventista_id = setup_preventista.id_preventista
    # Delete
    resp = client.delete(f"/api/v1/preventista/{preventista_id}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    # Verify deletion
    resp = client.get(f"/api/v1/preventista/{preventista_id}")
    assert resp.status_code == 404

