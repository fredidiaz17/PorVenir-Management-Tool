def test_get_deudas(client, setup_deuda):
    resp = client.get("/api/v1/deuda/")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"
    assert len(data["data"]) > 0

def test_get_deuda(client, setup_deuda):
    d = setup_deuda["deuda"]
    resp = client.get(f"/api/v1/deuda/{d.id_deuda}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_abono_deuda(client, setup_deuda):
    d = setup_deuda["deuda"]
    resp = client.post(f"/api/v1/deuda/{d.id_deuda}", json={
        "monto_abonado": 50.0
    })
    # If the backend router has an AttributeError bug, this might raise an error.
    # We assert that the status code is either successful (200) or handles validation.
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

def test_delete_deuda(client, setup_deuda):
    d = setup_deuda["deuda"]
    resp = client.delete(f"/api/v1/deuda/{d.id_deuda}")
    data = client.assert_status(resp, 200)
    assert data["status"] == "ok"

    resp = client.get(f"/api/v1/deuda/{d.id_deuda}")
    client.assert_status(resp, 404)
