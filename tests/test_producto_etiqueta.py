def test_create_producto_etiqueta(client, setup_producto_etiqueta, setup_etiqueta):
    # Create a product via API (needs a marca, which setup_marca provides)
    resp = client.post("/api/v1/producto_etiqueta/", json={
        "id_producto":setup_producto_etiqueta.id_producto,
        "id_etiqueta":setup_etiqueta.id_etiqueta, # Tocó usar setup_etiqueta para no violar constraint unico de producto_etiqueta
        "estado": "Activo"
        })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_producto_etiquetas(client, setup_producto_etiqueta, setup_etiqueta):
    resp = client.post("/api/v1/producto_etiqueta/", json={
        "id_producto":setup_producto_etiqueta.id_producto,
        "id_etiqueta":setup_etiqueta.id_etiqueta,
        "estado": "Activo"
        })

    # Retrieve list
    resp = client.get("/api/v1/producto_etiqueta/")
    assert resp.status_code == 200
    lst = resp.json()["data"]
    assert len(lst) >= 1

def test_get_producto_etiquetas_id(client, setup_producto_etiqueta):
    id_producto = setup_producto_etiqueta.producto.id_producto
    id_etiqueta = setup_producto_etiqueta.etiqueta.id_etiqueta

    # Retrieve specific relation
    resp = client.get(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}")
    assert resp.status_code == 200
    rel = resp.json()["data"]
    assert rel["id_producto"] == id_producto
    assert rel["id_etiqueta"] == id_etiqueta

def test_put_producto_etiqueta(client, setup_producto_etiqueta):
    id_producto = setup_producto_etiqueta.producto.id_producto
    id_etiqueta = setup_producto_etiqueta.etiqueta.id_etiqueta

    # Update (PUT) – change estado
    resp = client.put(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}", json={
        "id_producto": id_producto,
        "id_etiqueta": id_etiqueta,
        "estado": "Inactivo"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_delete_producto_etiqueta(client, setup_producto_etiqueta):
    id_producto = setup_producto_etiqueta.producto.id_producto
    id_etiqueta = setup_producto_etiqueta.etiqueta.id_etiqueta
    
    # Delete relation
    resp = client.delete(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    # Verify deletion
    resp = client.get(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}")
    assert resp.status_code == 404

