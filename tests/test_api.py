from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_recarga_valida():
    r = client.post("/recarga", json={"monto": 10000, "premium": False})
    assert r.status_code == 200
    data = r.json()
    assert data["bonificacion_pct"] == 10
    assert data["datos_mb"] == 1000

def test_recarga_premium():
    r = client.post("/recarga", json={"monto": 10000, "premium": True})
    assert r.status_code == 200
    assert r.json()["bonificacion_pct"] == 15

def test_recarga_monto_invalido_pydantic():
    r = client.post("/recarga", json={"monto": 500, "premium": False})
    assert r.status_code == 422

def test_recarga_monto_alto():
    r = client.post("/recarga", json={"monto": 60000, "premium": False})
    assert r.status_code == 422