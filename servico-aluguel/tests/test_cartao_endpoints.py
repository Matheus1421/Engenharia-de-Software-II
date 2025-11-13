"""
Testes unitários dos endpoints de cartão de crédito.
Cobre UC07 (Manter Cartão de Crédito) - CRUD completo.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app
from models.cartao_model import CartaoDeCredito

client = TestClient(app)


#   FIXTURES

@pytest.fixture
def cartao_exemplo():
    """Cartão de crédito padrão para testes"""
    return CartaoDeCredito(
        id=1,
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",
        cvv="123",
        idCiclista=1
    )


@pytest.fixture
def cartao_exemplo_2():
    """Segundo cartão de crédito para testes"""
    return CartaoDeCredito(
        id=2,
        nomeTitular="Maria Santos",
        numero="9876543210987654",
        validade="06/26",
        cvv="456",
        idCiclista=2
    )


@pytest.fixture
def dados_cartao_valido():
    """Dados válidos para criar novo cartão"""
    return {
        "nomeTitular": "Carlos Pereira",
        "numero": "5555666677778888",
        "validade": "03/27",
        "cvv": "789"
    }


#   TESTES GET /cartao

def test_listar_cartoes_sucesso(cartao_exemplo, cartao_exemplo_2):
    """UC07 - Testa listagem de todos os cartões"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.listar.return_value = [cartao_exemplo, cartao_exemplo_2]

        response = client.get("/cartao")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2
        mock_instance.listar.assert_called_once()


def test_listar_cartoes_lista_vazia():
    """UC07 - Testa listagem quando não há cartões"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.listar.return_value = []

        response = client.get("/cartao")

        assert response.status_code == 200
        assert response.json() == []


#   TESTES GET /cartao/{id}

def test_buscar_cartao_sucesso(cartao_exemplo):
    """UC07 - Testa busca de cartão por ID - sucesso"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_id.return_value = cartao_exemplo

        response = client.get("/cartao/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["nomeTitular"] == "João Silva"
        assert data["numero"] == "1234567890123456"
        mock_instance.buscar_por_id.assert_called_once_with(1)


def test_buscar_cartao_nao_encontrado():
    """UC07 - Testa erro ao buscar cartão inexistente"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_id.return_value = None

        response = client.get("/cartao/999")

        assert response.status_code == 404


#   TESTES POST /cartao

def test_cadastrar_cartao_sucesso(dados_cartao_valido):
    """UC07 - Testa cadastro de novo cartão - sucesso"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance

        # Cartão criado
        mock_instance.criar.return_value = CartaoDeCredito(
            id=3,
            nomeTitular="Carlos Pereira",
            numero="5555666677778888",
            validade="03/27",
            cvv="789",
            idCiclista=3
        )

        response = client.post("/cartao", json=dados_cartao_valido, params={"idCiclista": 3})

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 3
        assert data["nomeTitular"] == "Carlos Pereira"
        assert data["idCiclista"] == 3
        mock_instance.criar.assert_called_once()


def test_cadastrar_cartao_numero_invalido_curto():
    """UC07 - Testa erro quando número tem menos de 13 dígitos"""
    dados_invalidos = {
        "nomeTitular": "João Silva",
        "numero": "123456789012",  # 12 dígitos (menos que 13)
        "validade": "12/25",
        "cvv": "123"
    }

    response = client.post("/cartao", json=dados_invalidos, params={"idCiclista": 1})

    assert response.status_code == 422


def test_cadastrar_cartao_numero_invalido_longo():
    """UC07 - Testa erro quando número tem mais de 19 dígitos"""
    dados_invalidos = {
        "nomeTitular": "João Silva",
        "numero": "12345678901234567890",  # 20 dígitos (mais que 19)
        "validade": "12/25",
        "cvv": "123"
    }

    response = client.post("/cartao", json=dados_invalidos, params={"idCiclista": 1})

    assert response.status_code == 422


def test_cadastrar_cartao_validade_formato_invalido():
    """UC07 - Testa erro quando formato de validade é inválido"""
    dados_invalidos = {
        "nomeTitular": "João Silva",
        "numero": "1234567890123456",
        "validade": "12-25",  # Formato errado (deve ser MM/AA)
        "cvv": "123"
    }

    response = client.post("/cartao", json=dados_invalidos, params={"idCiclista": 1})

    assert response.status_code == 422


def test_cadastrar_cartao_cvv_invalido_curto():
    """UC07 - Testa erro quando CVV tem menos de 3 dígitos"""
    dados_invalidos = {
        "nomeTitular": "João Silva",
        "numero": "1234567890123456",
        "validade": "12/25",
        "cvv": "12"  # 2 dígitos
    }

    response = client.post("/cartao", json=dados_invalidos, params={"idCiclista": 1})

    assert response.status_code == 422


def test_cadastrar_cartao_cvv_invalido_longo():
    """UC07 - Testa erro quando CVV tem mais de 4 dígitos"""
    dados_invalidos = {
        "nomeTitular": "João Silva",
        "numero": "1234567890123456",
        "validade": "12/25",
        "cvv": "12345"  # 5 dígitos
    }

    response = client.post("/cartao", json=dados_invalidos, params={"idCiclista": 1})

    assert response.status_code == 422


def test_cadastrar_cartao_campos_faltando():
    """UC07 - Testa erro quando faltam campos obrigatórios"""
    dados_incompletos = {
        "nomeTitular": "João Silva"
        # Faltam outros campos
    }

    response = client.post("/cartao", json=dados_incompletos, params={"idCiclista": 1})

    assert response.status_code == 422


#   TESTES PUT /cartao/{id}

def test_atualizar_cartao_nao_encontrado():
    """UC07 - Testa erro ao atualizar cartão inexistente"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.atualizar.return_value = None

        dados_atualizacao = {
            "nomeTitular": "João Silva",
            "numero": "1234567890123456",
            "validade": "12/25",
            "cvv": "123"
        }

        response = client.put("/cartao/999", json=dados_atualizacao)

        assert response.status_code == 404


#   TESTES DELETE /cartao/{id}

def test_deletar_cartao_nao_encontrado():
    """UC07 - Testa erro ao remover cartão inexistente"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.deletar.return_value = False

        response = client.delete("/cartao/999")

        assert response.status_code == 404


#   TESTES GET /cartao/ciclista/{idCiclista}

def test_buscar_cartao_por_ciclista_nao_encontrado():
    """UC07 - Testa erro quando ciclista não tem cartão"""
    with patch('routers.cartao.get_db'), \
         patch('routers.cartao.CartaoRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_ciclista.return_value = None

        response = client.get("/cartao/ciclista/999")

        assert response.status_code == 404
