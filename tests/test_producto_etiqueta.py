def test_create_producto_etiqueta(client, setup_producto_etiqueta, setup_etiqueta):
    # Create a product via API (needs a marca, which setup_marca provides)
    resp = client.post("/api/v1/producto_etiqueta/", json={
        "id_producto":setup_producto_etiqueta["producto"].id_producto,
        "id_etiqueta":setup_producto_etiqueta["etiqueta_2"].id_etiqueta, # Tocó usar setup_etiqueta para no violar constraint unico de producto_etiqueta
        "estado": "Activo"
        })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_get_producto_etiquetas(client, setup_producto_etiqueta):
    resp = client.post("/api/v1/producto_etiqueta/", json={
        "id_producto":setup_producto_etiqueta["producto"].id_producto,
        "id_etiqueta":setup_producto_etiqueta["etiqueta_2"].id_etiqueta,
        "estado": "Activo"
        })

    # Retrieve list
    resp = client.get("/api/v1/producto_etiqueta/")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    lst = data["data"]
    assert len(lst) >= 1

def test_get_producto_etiquetas_id(client, setup_producto_etiqueta):
    id_producto = setup_producto_etiqueta["producto"].id_producto
    id_etiqueta = setup_producto_etiqueta["etiqueta_1"].id_etiqueta

    # Retrieve specific relation
    resp = client.get(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    rel = data["data"]
    assert rel["id_producto"] == id_producto
    assert rel["id_etiqueta"] == id_etiqueta

def test_put_producto_etiqueta(client, setup_producto_etiqueta):
    id_producto = setup_producto_etiqueta["producto"].id_producto
    id_etiqueta = setup_producto_etiqueta["etiqueta_1"].id_etiqueta

    # Update (PUT) – change estado
    resp = client.put(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}", json={
        "id_producto": id_producto,
        "id_etiqueta": id_etiqueta,
        "estado": "Inactivo"
    })
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_delete_producto_etiqueta(client, setup_producto_etiqueta):
    id_producto = setup_producto_etiqueta["producto"].id_producto
    id_etiqueta = setup_producto_etiqueta["etiqueta_1"].id_etiqueta
    
    # Delete relation
    resp = client.delete(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    # Verify deletion
    resp = client.get(f"/api/v1/producto_etiqueta/{id_producto}/{id_etiqueta}")
    client.assert_status(resp, 404)

