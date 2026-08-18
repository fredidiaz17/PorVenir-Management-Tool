def test_create_preventista(client, setup_preventista):
    # Create a preventista using the existing compania fixture
    resp = client.post("/api/v1/preventista/", json={
        "nombre": "TestPreventista",
        "telefono": "123456789",
        "id_compania": setup_preventista["compania"].id_compania
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_get_preventistas(client, setup_preventista):
    # List preventistas
    resp = client.post("/api/v1/preventista/", json={
        "nombre": "TestPreventista",    
        "telefono": "123456789",
        "id_compania": setup_preventista["compania"].id_compania
    })
    resp = client.get("/api/v1/preventista/")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    lst = data["data"]
    assert len(lst) >= 2
    assert any(p["nombre"] == "TestPreventista" for p in lst)

def test_get_preventista_id(client, setup_preventista):
    # Get by ID
    preventista_id = setup_preventista["preventista"].id_preventista
    resp = client.get(f"/api/v1/preventista/{preventista_id}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == setup_preventista["preventista"].nombre

def test_update_preventista(client, setup_preventista):
    preventista_id = setup_preventista["preventista"].id_preventista
    # Update (PUT)
    resp = client.put(f"/api/v1/preventista/{preventista_id}", json={
        "nombre": "UpdatedPreventista",
        "telefono": "987654321",
        "id_compania": setup_preventista["compania"].id_compania
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    resp = client.get(f"/api/v1/preventista/{preventista_id}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == "UpdatedPreventista"

def test_patch_preventista(client, setup_preventista):
    preventista_id = setup_preventista["preventista"].id_preventista
    
    resp = client.patch(f"/api/v1/preventista/{preventista_id}", json={
        "telefono": "987654321",
    })

    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    resp = client.get(f"/api/v1/preventista/{preventista_id}") 
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert data["data"]["telefono"] == "987654321"
    
def test_delete_preventista(client, setup_preventista):
    preventista_id = setup_preventista["preventista"].id_preventista
    # Delete
    resp = client.delete(f"/api/v1/preventista/{preventista_id}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    # Verify deletion
    resp = client.get(f"/api/v1/preventista/{preventista_id}")
    client.assert_status(resp, 404)

