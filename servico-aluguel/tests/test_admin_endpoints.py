"""Testes para routers/admin.py"""
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_restaurar_banco_sucesso():
    """Testa endpoint de restaurar banco de dados"""
    with patch('routers.admin.reset_db'), \
         patch('routers.admin.get_db'), \
         patch('routers.admin.init_db'):

        response = client.get("/restaurarBanco")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "restaurado" in data["message"].lower()
