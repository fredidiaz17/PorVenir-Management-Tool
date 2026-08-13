def test_create_pedido(client, setup_pedido):
    id_preventista = setup_pedido["preventista"].id_preventista
    producto_id = setup_pedido["producto"].id_producto
    resp = client.post("/api/v1/pedido/", json={
        "fecha_pedido": "2026-08-05",
        "estado": "Pendiente",
        "subtotal": 50.0,
        "impuestos": 9.5,
        "total": 59.5,
        "id_preventista": id_preventista,
        "detalles_pedido": [
            {
                "id_producto": producto_id,
                "cantidad": 5.0,
                "precio_unitario": 10.0,
                "subtotal_linea": 50.0,
                "iva_porcentaje": 0.19,
                "iva_valor": 9.5,
                "total_linea": 59.5
            }
        ]
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"



def test_get_pedidos(client, setup_pedido):
    resp = client.get("/api/v1/pedido/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert len(resp.json()["data"]) > 0


def test_get_pedido(client, setup_pedido):
    id_pedido = setup_pedido["pedido"].id_pedido
    resp = client.get(f"/api/v1/pedido/{id_pedido}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_update_pedido(client, setup_pedido):
    id_pedido = setup_pedido["pedido"].id_pedido
    id_preventista = setup_pedido["preventista"].id_preventista
    producto_id = setup_pedido["producto"].id_producto
    resp = client.put(f"/api/v1/pedido/{id_pedido}", json={
        "fecha_pedido": "2026-08-05",
        "estado": "En camino",
        "subtotal": 60.0,
        "impuestos": 11.4,
        "total": 71.4,
        "id_preventista": id_preventista,
        "detalles_pedido": [
            {
                "id_producto": producto_id,
                "cantidad": 6.0,
                "precio_unitario": 10.0,
                "subtotal_linea": 60.0,
                "iva_porcentaje": 0.19,
                "iva_valor": 11.4,
                "total_linea": 71.4
            }
        ]
    })
    print(resp.json())
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_patch_pedido(client, setup_pedido):
    id_pedido = setup_pedido["pedido"].id_pedido
    resp = client.patch(f"/api/v1/pedido/{id_pedido}", json={
        "estado": "Recibido"
    })
    print(resp.json())
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_delete_pedido(client, setup_pedido):
    id_pedido = setup_pedido["pedido"].id_pedido
    resp = client.delete(f"/api/v1/pedido/{id_pedido}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    resp = client.get(f"/api/v1/pedido/{id_pedido}")
    assert resp.status_code == 404
