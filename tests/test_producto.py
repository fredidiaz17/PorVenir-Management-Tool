def test_create_producto(client, setup_producto):
    id_marca = setup_producto["marca"].id_marca
    response = client.post("/api/v1/producto/", json={
        "nombre": "Test Producto",
        "precio_compra": 10.0,
        "precio_venta": 15.0,
        "id_marca": id_marca,
        "cantidad_stock": 100,
        "unidad_medida": "Unidades",
        "porcentaje_iva": 0.19
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_get_productos(client, setup_producto):
    id_marca = setup_producto["marca"].id_marca
    response = client.post("/api/v1/producto/", json={
        "nombre": "Test Producto",
        "precio_compra": 10.0,
        "precio_venta": 15.0,
        "id_marca": id_marca,
        "cantidad_stock": 100,
        "unidad_medida": "Unidades",
        "porcentaje_iva": 0.19
    })

    response = client.get("/api/v1/producto/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["data"]) >= 2

def test_get_producto_by_id(client, setup_producto):
    id_producto = setup_producto["producto"].id_producto
    nombre_producto = setup_producto["producto"].nombre
    response = client.get(f"/api/v1/producto/{id_producto}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["data"]["nombre"] == nombre_producto

def test_update_producto(client, setup_producto):
    id_producto = setup_producto["producto"].id_producto
    response = client.put(f"/api/v1/producto/{id_producto}", json={
        "nombre": "Updated Producto",
        "precio_compra": 12.0,
        "precio_venta": 18.0,
        "id_marca": 1,
        "cantidad_stock": 50,
        "unidad_medida": "Unidades",
        "porcentaje_iva": 0.21
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get(f"/api/v1/producto/{id_producto}")
    assert get_response.json()["data"]["nombre"] == "Updated Producto"

def test_update_producto_parcial(client, setup_producto):
    id_producto = setup_producto["producto"].id_producto    
    response = client.patch(f"/api/v1/producto/{id_producto}", json={
        "nombre": "Parcial Update",
        "precio_venta": 20.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get(f"/api/v1/producto/{id_producto}")
    assert get_response.json()["data"]["precio_venta"] == 20.0
    assert get_response.json()["data"]["nombre"] == "Parcial Update"

def test_delete_producto(client, setup_producto):
    id_producto = setup_producto["producto"].id_producto    
    response = client.delete(f"/api/v1/producto/{id_producto}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    
    get_response = client.get(f"/api/v1/producto/{id_producto}")
    assert get_response.status_code == 404
