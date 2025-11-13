"""
Teste básico do endpoint de status.
Valida que o servidor está respondendo corretamente.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_status_retorna_200():
    """Testa que o endpoint /status retorna 200 OK"""
    response = client.get("/status")
    assert response.status_code == 200


def test_status_retorna_mensagem():
    """Testa que o endpoint /status retorna mensagem ou status no JSON"""
    response = client.get("/status")
    data = response.json()

    # O endpoint deve retornar pelo menos um desses campos
    assert "mensagem" in data or "status" in data
