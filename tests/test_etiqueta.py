def test_create_etiqueta(client, setup_etiqueta):
    # Create
    resp = client.post("/api/v1/etiqueta/", json={
        "nombre_etiqueta": "TestEtiqueta",
        "descripcion_etiqueta": "Descripción",
        "color_hex": "#FF5733"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"

def test_get_etiquetas(client, setup_etiqueta):
    resp = client.post("/api/v1/etiqueta/", json={
        "nombre_etiqueta": "TestEtiqueta",
        "descripcion_etiqueta": "Descripción",
        "color_hex": "#FF5733"
    })
    nombre_etiqueta = setup_etiqueta["etiqueta"].nombre_etiqueta 
    
    resp = client.get("/api/v1/etiqueta/")
    assert resp.status_code == 200
    lst = resp.json()["data"]
    assert len(lst) >= 2
    assert any(e["nombre_etiqueta"] == nombre_etiqueta for e in lst)

def test_get_etiqueta(client, setup_etiqueta):
    nombre_etiqueta = setup_etiqueta["etiqueta"].nombre_etiqueta 
    etiqueta_id = setup_etiqueta["etiqueta"].id_etiqueta

    resp = client.get(f"/api/v1/etiqueta/{etiqueta_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["nombre_etiqueta"] == nombre_etiqueta


def test_update_etiqueta(client, setup_etiqueta):
    etiqueta_id = setup_etiqueta["etiqueta"].id_etiqueta
    resp = client.put(f"/api/v1/etiqueta/{etiqueta_id}", json={
        "nombre_etiqueta": "UpdatedEtiqueta",
        "descripcion_etiqueta": "Nueva descripción",
        "color_hex": "#123456"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_patch_etiqueta(client, setup_etiqueta):
    etiqueta_id = setup_etiqueta["etiqueta"].id_etiqueta
    
    resp = client.patch(f"/api/v1/etiqueta/{etiqueta_id}", json={"color_hex": "#ABCDEF"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_delete_etiqueta(client, setup_etiqueta):
    etiqueta_id = setup_etiqueta["etiqueta"].id_etiqueta
    resp = client.delete(f"/api/v1/etiqueta/{etiqueta_id}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    # Verify deletion
    resp = client.get(f"/api/v1/etiqueta/{etiqueta_id}")
    assert resp.status_code == 404
