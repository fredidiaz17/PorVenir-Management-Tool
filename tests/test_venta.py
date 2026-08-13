def test_create_venta(client, setup_venta):
    c = setup_venta["cliente"]
    p = setup_venta["producto"]
    resp = client.post("/api/v1/venta/", json={
        "fecha": "2026-08-13",
        "medio_pago": "Efectivo",
        "total": 20.0,
        "id_cliente": c.id_cliente,
        "detalles_venta": [
            {
                "id_producto": p.id_producto,
                "cantidad": 2.0,
                "precio_venta": 10.0,
                "descuento_manual": 0.0,
                "subtotal": 20.0
            }
        ]
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_create_venta_fiado(client, setup_venta):
    c = setup_venta["cliente"]
    p = setup_venta["producto"]
    resp = client.post("/api/v1/venta/", json={
        "fecha": "2026-08-13",
        "medio_pago": "Fiado",
        "total": 50.0,
        "id_cliente": c.id_cliente,
        "detalles_venta": [
            {
                "id_producto": p.id_producto,
                "cantidad": 5.0,
                "precio_venta": 10.0,
                "descuento_manual": 0.0,
                "subtotal": 50.0
            }
        ]
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_ventas(client, setup_venta):
    resp = client.get("/api/v1/venta/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert len(resp.json()["data"]) > 0

def test_get_venta(client, setup_venta):
    v = setup_venta["venta"]
    resp = client.get(f"/api/v1/venta/{v.id_venta}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_anular_venta(client, setup_venta):
    v = setup_venta["venta"]
    resp = client.post(f"/api/v1/venta/{v.id_venta}/anular")
    print(resp.json())
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_delete_venta(client, setup_venta):
    v = setup_venta["venta"]
    resp = client.delete(f"/api/v1/venta/{v.id_venta}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    resp = client.get(f"/api/v1/venta/{v.id_venta}")
    assert resp.status_code == 404
