"""
Testes unitários para os endpoints de cobranças.
Cobre todos os cenários de sucesso e erro dos endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock

from main import app
from models.cobranca_model import Cobranca, NovaCobranca, StatusCobranca, ProcessarPagamentoRequest


client = TestClient(app)


# ==================== FIXTURES ====================

@pytest.fixture
def mock_db():
    """Mock do banco de dados"""
    return MagicMock()


@pytest.fixture
def cobranca_exemplo():
    """Cobrança de exemplo para testes"""
    return Cobranca(
        id=1,
        id_ciclista=1,
        valor=50.00,
        status=StatusCobranca.PENDENTE,
        data_criacao="2024-01-15T10:00:00Z",
        data_vencimento="2024-02-15T10:00:00Z",
        data_pagamento=None,
        descricao="Mensalidade do mês de janeiro"
    )


@pytest.fixture
def cobranca_paga():
    """Cobrança já paga de exemplo"""
    return Cobranca(
        id=1,
        id_ciclista=1,
        valor=50.00,
        status=StatusCobranca.PAGA,
        data_criacao="2024-01-15T10:00:00Z",
        data_vencimento="2024-02-15T10:00:00Z",
        data_pagamento="2024-01-20T10:00:00Z",
        descricao="Mensalidade do mês de janeiro"
    )


@pytest.fixture
def nova_cobranca_valida():
    """Dados válidos para criar nova cobrança"""
    return {
        "idCiclista": 1,
        "valor": 75.50,
        "dataVencimento": "2024-03-15T10:00:00Z",
        "descricao": "Mensalidade do mês de fevereiro"
    }


# ==================== TESTES POST /cobranca (contrato externo) ====================

def test_criar_cobranca_sucesso(nova_cobranca_valida):
    """Testa criação de nova cobrança - sucesso"""
    with patch('routers.cobranca.get_db'), \
         patch('routers.cobranca.CobrancaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.create.return_value = Cobranca(
            id=1,
            id_ciclista=nova_cobranca_valida["idCiclista"],
            valor=nova_cobranca_valida["valor"],
            status=StatusCobranca.PENDENTE,
            data_criacao="2024-01-15T10:00:00Z",
            data_vencimento=nova_cobranca_valida["dataVencimento"],
            data_pagamento=None,
            descricao=nova_cobranca_valida["descricao"]
        )
        
        response = client.post("/cobranca", json=nova_cobranca_valida)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["valor"] == 75.50
        assert response.json()["status"] == "PENDENTE"
        mock_repo_instance.create.assert_called_once()


def test_criar_cobranca_dados_invalidos():
    """Testa erro ao criar cobrança com dados inválidos"""
    cobranca_invalida = {
        "idCiclista": 1,
        "valor": -10.00,  # Valor negativo
        "dataVencimento": "2024-03-15T10:00:00Z",
        "descricao": "Descrição"
    }
    
    response = client.post("/cobranca", json=cobranca_invalida)
    
    assert response.status_code == 422


def test_criar_cobranca_campos_faltando():
    """Testa erro ao criar cobrança sem campos obrigatórios"""
    cobranca_incompleta = {
        "idCiclista": 1
        # Faltam outros campos
    }
    
    response = client.post("/cobranca", json=cobranca_incompleta)
    
    assert response.status_code == 422


# ==================== TESTES GET /cobranca/{id_cobranca} ====================

def test_obter_cobranca_sucesso(cobranca_exemplo):
    """Testa obtenção de cobrança por ID - sucesso"""
    with patch('routers.cobranca.get_db'), \
         patch('routers.cobranca.CobrancaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = cobranca_exemplo
        
        response = client.get("/cobranca/1")
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["valor"] == 50.00
        assert response.json()["status"] == "PENDENTE"
        mock_repo_instance.get_by_id.assert_called_once_with(1)


def test_obter_cobranca_nao_encontrada():
    """Testa erro ao buscar cobrança inexistente"""
    with patch('routers.cobranca.get_db'), \
         patch('routers.cobranca.CobrancaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.get("/cobranca/999")
        
        assert response.status_code == 404
        assert "COBRANCA_NAO_ENCONTRADA" in str(response.json())


def test_criar_cobranca_exception_generica(nova_cobranca_valida):
    """Testa tratamento de exceção genérica na criação"""
    with patch('routers.cobranca.get_db'), \
         patch('routers.cobranca.CobrancaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.create.side_effect = Exception("Erro no banco")
        
        response = client.post("/cobranca", json=nova_cobranca_valida)
        
        assert response.status_code == 422
        assert "DADOS_INVALIDOS" in str(response.json())

