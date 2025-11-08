"""
Testes unitários para os endpoints de trancas.
Cobertura completa de todos os 11 endpoints com validações.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from models.tranca_model import Tranca, NovaTranca, StatusTranca
from models.bicicleta_model import Bicicleta, StatusBicicleta
from models.totem_model import Totem


client = TestClient(app)


# ========== FIXTURES ==========

@pytest.fixture
def tranca_exemplo():
    """Tranca de exemplo para testes"""
    return Tranca(
        id=1,
        numero=1,
        localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023",
        modelo="Modelo X1",
        status=StatusTranca.LIVRE,
        bicicleta=None
    )


@pytest.fixture
def tranca_exemplo_2():
    """Segunda tranca de exemplo"""
    return Tranca(
        id=2,
        numero=2,
        localizacao="-22.9100,-43.1800",
        anoDeFabricacao="2023",
        modelo="Modelo X2",
        status=StatusTranca.LIVRE,
        bicicleta=None
    )


@pytest.fixture
def tranca_ocupada():
    """Tranca ocupada com bicicleta"""
    return Tranca(
        id=3,
        numero=3,
        localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023",
        modelo="Modelo X1",
        status=StatusTranca.OCUPADA,
        bicicleta=1
    )


@pytest.fixture
def tranca_nova():
    """Tranca com status NOVA"""
    return Tranca(
        id=4,
        numero=4,
        localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2024",
        modelo="Modelo X1",
        status=StatusTranca.NOVA,
        bicicleta=None
    )


@pytest.fixture
def tranca_em_reparo():
    """Tranca em reparo"""
    return Tranca(
        id=5,
        numero=5,
        localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023",
        modelo="Modelo X1",
        status=StatusTranca.EM_REPARO,
        bicicleta=None
    )


@pytest.fixture
def nova_tranca_valida():
    """Dados válidos para criar nova tranca"""
    return {
        "numero": 10,
        "localizacao": "-22.9068,-43.1729",
        "anoDeFabricacao": "2024",
        "modelo": "Modelo X1",
        "status": "NOVA"
    }


@pytest.fixture
def bicicleta_exemplo():
    """Bicicleta de exemplo"""
    return Bicicleta(
        id=1,
        marca="Caloi",
        modelo="Mountain Bike",
        ano="2023",
        numero=101,
        status=StatusBicicleta.DISPONIVEL
    )


@pytest.fixture
def totem_exemplo():
    """Totem de exemplo"""
    return Totem(
        id=1,
        localizacao="-22.9068,-43.1729",
        descricao="Totem Central"
    )


# ========== TESTES GET /tranca ==========

def test_listar_trancas_sucesso(tranca_exemplo, tranca_exemplo_2):
    """Testa listagem de trancas com sucesso"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_all.return_value = [tranca_exemplo, tranca_exemplo_2]
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2


def test_listar_trancas_vazio():
    """Testa listagem quando não há trancas"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_all.return_value = []
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca")
        
        assert response.status_code == 200
        assert response.json() == []


def test_listar_trancas_multiplas():
    """Testa listagem com múltiplas trancas"""
    trancas = [
        Tranca(id=i, numero=i, localizacao="-22.9068,-43.1729", 
               anoDeFabricacao="2023", modelo=f"Modelo X{i}", 
               status=StatusTranca.LIVRE, bicicleta=None)
        for i in range(1, 6)
    ]
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_all.return_value = trancas
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5


# ========== TESTES POST /tranca ==========

def test_cadastrar_tranca_sucesso(nova_tranca_valida):
    """Testa cadastro de tranca com sucesso"""
    tranca_criada = Tranca(id=1, **{**nova_tranca_valida, "status": StatusTranca.NOVA, "bicicleta": None})
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_all.return_value = []
        mock_repo_instance.create.return_value = tranca_criada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca", json=nova_tranca_valida)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["numero"] == 10
        assert data["modelo"] == "Modelo X1"


def test_cadastrar_tranca_numero_duplicado(nova_tranca_valida, tranca_exemplo):
    """Testa erro ao cadastrar tranca com número duplicado"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_all.return_value = [tranca_exemplo]
        mock_repo.return_value = mock_repo_instance
        
        nova_tranca = {**nova_tranca_valida, "numero": 1}  # Número já existe
        response = client.post("/tranca", json=nova_tranca)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert data["detail"][0]["codigo"] == "NUMERO_DUPLICADO"


def test_cadastrar_tranca_dados_invalidos():
    """Testa erro com dados inválidos"""
    tranca_invalida = {
        "numero": -1,  # Número inválido
        "localizacao": "",
        "anoDeFabricacao": "abc",
        "modelo": "",
        "status": "INVALIDO"
    }
    
    response = client.post("/tranca", json=tranca_invalida)
    
    assert response.status_code == 422


def test_cadastrar_tranca_sem_numero():
    """Testa erro ao cadastrar sem número"""
    tranca_sem_numero = {
        "localizacao": "-22.9068,-43.1729",
        "anoDeFabricacao": "2024",
        "modelo": "Modelo X1",
        "status": "NOVA"
    }
    
    response = client.post("/tranca", json=tranca_sem_numero)
    
    assert response.status_code == 422


def test_cadastrar_tranca_exception():
    """Testa tratamento de exceção no cadastro"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_all.side_effect = Exception("Erro de banco")
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca", json={"numero": 1, "localizacao": "-22.9,-43.1", "anoDeFabricacao": "2024", "modelo": "X1", "status": "NOVA"})
        
        assert response.status_code == 422


# ========== TESTES GET /tranca/{idTranca} ==========

def test_obter_tranca_sucesso(tranca_exemplo):
    """Testa obtenção de tranca com sucesso"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["numero"] == 1


def test_obter_tranca_nao_encontrada():
    """Testa erro quando tranca não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca/999")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"]["codigo"] == "TRANCA_NAO_ENCONTRADA"


def test_obter_tranca_id_zero():
    """Testa obtenção de tranca com ID zero"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca/0")
        
        assert response.status_code == 404


# ========== TESTES PUT /tranca/{idTranca} ==========

def test_editar_tranca_sucesso(tranca_exemplo):
    """Testa edição de tranca com sucesso"""
    dados_atualizados = {
        "numero": 1,
        "localizacao": "-22.9068,-43.1729",
        "anoDeFabricacao": "2023",
        "modelo": "Modelo X1 ATUALIZADO",
        "status": "LIVRE"
    }
    
    tranca_atualizada = Tranca(id=1, **{**dados_atualizados, "status": StatusTranca.LIVRE, "bicicleta": None})
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_instance.get_all.return_value = [tranca_exemplo]
        mock_repo_instance.update.return_value = tranca_atualizada
        mock_repo.return_value = mock_repo_instance
        
        response = client.put("/tranca/1", json=dados_atualizados)
        
        assert response.status_code == 200
        data = response.json()
        assert data["modelo"] == "Modelo X1 ATUALIZADO"


def test_editar_tranca_nao_encontrada():
    """Testa erro ao editar tranca inexistente"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        dados = {
            "numero": 1,
            "localizacao": "-22.9068,-43.1729",
            "anoDeFabricacao": "2023",
            "modelo": "Modelo X1",
            "status": "LIVRE"
        }
        
        response = client.put("/tranca/999", json=dados)
        
        assert response.status_code == 404


def test_editar_tranca_numero_duplicado(tranca_exemplo, tranca_exemplo_2):
    """Testa erro ao alterar número para um já existente"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_instance.get_all.return_value = [tranca_exemplo, tranca_exemplo_2]
        mock_repo.return_value = mock_repo_instance
        
        dados = {
            "numero": 2,  # Número da tranca_exemplo_2
            "localizacao": "-22.9068,-43.1729",
            "anoDeFabricacao": "2023",
            "modelo": "Modelo X1",
            "status": "LIVRE"
        }
        
        response = client.put("/tranca/1", json=dados)
        
        assert response.status_code == 422


def test_editar_tranca_dados_invalidos(tranca_exemplo):
    """Testa erro com dados inválidos na edição"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo.return_value = mock_repo_instance
        
        dados_invalidos = {
            "numero": -1,
            "localizacao": "",
            "anoDeFabricacao": "abc",
            "modelo": "",
            "status": "INVALIDO"
        }
        
        response = client.put("/tranca/1", json=dados_invalidos)
        
        assert response.status_code == 422


def test_editar_tranca_exception(tranca_exemplo):
    """Testa tratamento de exceção na edição"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_instance.get_all.side_effect = Exception("Erro de banco")
        mock_repo.return_value = mock_repo_instance
        
        dados = {
            "numero": 1,
            "localizacao": "-22.9068,-43.1729",
            "anoDeFabricacao": "2023",
            "modelo": "Modelo X1",
            "status": "LIVRE"
        }
        
        response = client.put("/tranca/1", json=dados)
        
        assert response.status_code == 422


# ========== TESTES DELETE /tranca/{idTranca} ==========

def test_remover_tranca_sucesso():
    """Testa remoção de tranca com sucesso"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.delete.return_value = True
        mock_repo.return_value = mock_repo_instance
        
        response = client.delete("/tranca/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "mensagem" in data


def test_remover_tranca_nao_encontrada():
    """Testa erro ao remover tranca inexistente"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.delete.return_value = False
        mock_repo.return_value = mock_repo_instance
        
        response = client.delete("/tranca/999")
        
        assert response.status_code == 404


def test_remover_tranca_verifica_exclusao():
    """Testa se a tranca foi realmente excluída"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.delete.return_value = True
        mock_repo.return_value = mock_repo_instance
        
        response = client.delete("/tranca/1")
        
        assert response.status_code == 200
        mock_repo_instance.delete.assert_called_once_with(1)


# ========== TESTES GET /tranca/{idTranca}/bicicleta ==========

def test_obter_bicicleta_na_tranca_sucesso(tranca_ocupada, bicicleta_exemplo):
    """Testa obtenção de bicicleta na tranca"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        response = client.get("/tranca/3/bicicleta")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1


def test_obter_bicicleta_tranca_nao_encontrada():
    """Testa erro quando tranca não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca/999/bicicleta")
        
        assert response.status_code == 404


def test_obter_bicicleta_tranca_sem_bicicleta(tranca_exemplo):
    """Testa erro quando tranca não tem bicicleta"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/tranca/1/bicicleta")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"]["codigo"] == "BICICLETA_NAO_ENCONTRADA"


def test_obter_bicicleta_id_invalido_zero():
    """Testa erro com ID zero"""
    response = client.get("/tranca/0/bicicleta")
    
    assert response.status_code == 422
    data = response.json()
    assert data["detail"]["codigo"] == "ID_INVALIDO"


def test_obter_bicicleta_id_invalido_negativo():
    """Testa erro com ID negativo"""
    response = client.get("/tranca/-1/bicicleta")
    
    assert response.status_code == 422


def test_obter_bicicleta_nao_encontrada_no_banco(tranca_ocupada):
    """Testa erro quando bicicleta associada não existe no banco"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = None
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        response = client.get("/tranca/3/bicicleta")
        
        assert response.status_code == 404


# ========== TESTES POST /tranca/{idTranca}/trancar ==========

def test_trancar_sem_bicicleta(tranca_exemplo):
    """Testa trancamento sem bicicleta"""
    tranca_trancada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.OCUPADA, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_instance.update_status.return_value = tranca_trancada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/1/trancar", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OCUPADA"


def test_trancar_com_bicicleta(tranca_exemplo, bicicleta_exemplo):
    """Testa trancamento com bicicleta"""
    tranca_trancada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.OCUPADA, bicicleta=1
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca_instance.associar_bicicleta.return_value = None
        mock_repo_tranca_instance.update_status.return_value = tranca_trancada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_bicicleta_instance.update_status.return_value = None
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        response = client.post("/tranca/1/trancar", json={"bicicleta": 1})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OCUPADA"
        assert data["bicicleta"] == 1


def test_trancar_tranca_nao_encontrada():
    """Testa erro ao trancar tranca inexistente"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/999/trancar", json={})
        
        assert response.status_code == 404


def test_trancar_tranca_ja_trancada(tranca_ocupada):
    """Testa erro ao trancar tranca já trancada"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_ocupada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/3/trancar", json={})
        
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["codigo"] == "TRANCA_JA_TRANCADA"


def test_trancar_bicicleta_nao_encontrada(tranca_exemplo):
    """Testa erro quando bicicleta não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = None
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        response = client.post("/tranca/1/trancar", json={"bicicleta": 999})
        
        assert response.status_code == 404


# ========== TESTES POST /tranca/{idTranca}/destrancar ==========

def test_destrancar_sem_bicicleta(tranca_ocupada):
    """Testa destrancamento sem bicicleta"""
    tranca_destrancada = Tranca(
        id=3, numero=3, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.LIVRE, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_instance.update_status.return_value = tranca_destrancada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/3/destrancar", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "LIVRE"


def test_destrancar_com_bicicleta(tranca_ocupada, bicicleta_exemplo):
    """Testa destrancamento com bicicleta"""
    tranca_destrancada = Tranca(
        id=3, numero=3, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.LIVRE, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_tranca_instance.associar_bicicleta.return_value = None
        mock_repo_tranca_instance.update_status.return_value = tranca_destrancada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_bicicleta_instance.update_status.return_value = None
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        response = client.post("/tranca/3/destrancar", json={"bicicleta": 1})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "LIVRE"


def test_destrancar_tranca_nao_encontrada():
    """Testa erro ao destrancar tranca inexistente"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/999/destrancar", json={})
        
        assert response.status_code == 404


def test_destrancar_bicicleta_nao_encontrada(tranca_ocupada):
    """Testa erro quando bicicleta não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = None
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        response = client.post("/tranca/3/destrancar", json={"bicicleta": 999})
        
        assert response.status_code == 404


def test_destrancar_bicicleta_nao_esta_na_tranca(tranca_ocupada, bicicleta_exemplo):
    """Testa erro quando bicicleta não está na tranca"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.BicicletaRepository') as mock_repo_bicicleta:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_bicicleta_instance = MagicMock()
        mock_repo_bicicleta_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_bicicleta.return_value = mock_repo_bicicleta_instance
        
        # tranca_ocupada tem bicicleta 1, tentando destrancar com bicicleta 2
        response = client.post("/tranca/3/destrancar", json={"bicicleta": 2})
        
        assert response.status_code == 422


# ========== TESTES POST /tranca/{idTranca}/status/{acao} ==========

def test_alterar_status_trancar(tranca_exemplo):
    """Testa alteração de status para TRANCAR"""
    tranca_trancada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.OCUPADA, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_instance.update_status.return_value = tranca_trancada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/1/status/TRANCAR")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OCUPADA"


def test_alterar_status_destrancar(tranca_ocupada):
    """Testa alteração de status para DESTRANCAR"""
    tranca_destrancada = Tranca(
        id=3, numero=3, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.LIVRE, bicicleta=1
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_ocupada
        mock_repo_instance.update_status.return_value = tranca_destrancada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/3/status/DESTRANCAR")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "LIVRE"


def test_alterar_status_tranca_nao_encontrada():
    """Testa erro ao alterar status de tranca inexistente"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = None
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/999/status/TRANCAR")
        
        assert response.status_code == 404


def test_alterar_status_acao_invalida(tranca_exemplo):
    """Testa erro com ação inválida"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/1/status/INVALIDA")
        
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["codigo"] == "ACAO_INVALIDA"


def test_alterar_status_trancar_ja_trancada(tranca_ocupada):
    """Testa erro ao trancar tranca já trancada"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_ocupada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/3/status/TRANCAR")
        
        assert response.status_code == 422


def test_alterar_status_case_insensitive(tranca_exemplo):
    """Testa que ação aceita case insensitive"""
    tranca_trancada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.OCUPADA, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo:
        
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_instance.update_status.return_value = tranca_trancada
        mock_repo.return_value = mock_repo_instance
        
        response = client.post("/tranca/1/status/trancar")
        
        assert response.status_code == 200


# ========== TESTES POST /tranca/integrarNaRede ==========

def test_integrar_tranca_na_rede_sucesso(tranca_nova, totem_exemplo):
    """Testa integração de tranca na rede com sucesso"""
    tranca_integrada = Tranca(
        id=4, numero=4, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2024", modelo="Modelo X1",
        status=StatusTranca.LIVRE, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_nova
        mock_repo_tranca_instance.associar_totem.return_value = True
        mock_repo_tranca_instance.update_status.return_value = tranca_integrada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 4,
            "idFuncionario": 1
        }
        
        response = client.post("/tranca/integrarNaRede", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "mensagem" in data
        assert data["idTranca"] == 4
        assert data["idTotem"] == 1


def test_integrar_tranca_em_reparo(tranca_em_reparo, totem_exemplo):
    """Testa integração de tranca EM_REPARO"""
    tranca_integrada = Tranca(
        id=5, numero=5, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.LIVRE, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_em_reparo
        mock_repo_tranca_instance.associar_totem.return_value = True
        mock_repo_tranca_instance.update_status.return_value = tranca_integrada
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 5,
            "idFuncionario": 1
        }
        
        response = client.post("/tranca/integrarNaRede", json=request_data)
        
        assert response.status_code == 200


def test_integrar_tranca_nao_encontrada(totem_exemplo):
    """Testa erro quando tranca não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = None
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 999,
            "idFuncionario": 1
        }
        
        response = client.post("/tranca/integrarNaRede", json=request_data)
        
        assert response.status_code == 404


def test_integrar_totem_nao_encontrado(tranca_nova):
    """Testa erro quando totem não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_nova
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = None
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 999,
            "idTranca": 4,
            "idFuncionario": 1
        }
        
        response = client.post("/tranca/integrarNaRede", json=request_data)
        
        assert response.status_code == 404


def test_integrar_status_invalido(tranca_exemplo, totem_exemplo):
    """Testa erro ao integrar tranca com status inválido"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo  # Status LIVRE
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 1,
            "idFuncionario": 1
        }
        
        response = client.post("/tranca/integrarNaRede", json=request_data)
        
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["codigo"] == "STATUS_TRANCA_INVALIDO"


# ========== TESTES POST /tranca/retirarDaRede ==========

def test_retirar_tranca_da_rede_para_reparo(tranca_exemplo, totem_exemplo):
    """Testa retirada de tranca para reparo"""
    tranca_retirada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.EM_REPARO, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca_instance.get_totem_id.return_value = 1
        mock_repo_tranca_instance.update_status.return_value = tranca_retirada
        mock_repo_tranca_instance.desassociar_totem.return_value = True
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 1,
            "idFuncionario": 1,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "mensagem" in data
        assert data["novoStatus"] == "EM_REPARO"


def test_retirar_tranca_da_rede_para_aposentadoria(tranca_exemplo, totem_exemplo):
    """Testa retirada de tranca para aposentadoria"""
    tranca_retirada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.APOSENTADA, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca_instance.get_totem_id.return_value = 1
        mock_repo_tranca_instance.update_status.return_value = tranca_retirada
        mock_repo_tranca_instance.desassociar_totem.return_value = True
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 1,
            "idFuncionario": 1,
            "statusAcaoReparador": "APOSENTADA"
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["novoStatus"] == "APOSENTADA"


def test_retirar_tranca_nao_encontrada(totem_exemplo):
    """Testa erro quando tranca não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = None
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 999,
            "idFuncionario": 1,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 404


def test_retirar_totem_nao_encontrado(tranca_exemplo):
    """Testa erro quando totem não existe"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = None
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 999,
            "idTranca": 1,
            "idFuncionario": 1,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 404


def test_retirar_tranca_nao_esta_no_totem(tranca_exemplo, totem_exemplo):
    """Testa erro quando tranca não está no totem informado"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca_instance.get_totem_id.return_value = 2  # Tranca está em totem 2
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,  # Tentando retirar de totem 1
            "idTranca": 1,
            "idFuncionario": 1,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["codigo"] == "TRANCA_NAO_ESTA_NO_TOTEM"


def test_retirar_status_destino_invalido(tranca_exemplo, totem_exemplo):
    """Testa erro com status de destino inválido"""
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca_instance.get_totem_id.return_value = 1
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 1,
            "idFuncionario": 1,
            "statusAcaoReparador": "INVALIDO"
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["codigo"] == "STATUS_DESTINO_INVALIDO"


def test_retirar_case_insensitive_status(tranca_exemplo, totem_exemplo):
    """Testa que status aceita case insensitive"""
    tranca_retirada = Tranca(
        id=1, numero=1, localizacao="-22.9068,-43.1729",
        anoDeFabricacao="2023", modelo="Modelo X1",
        status=StatusTranca.EM_REPARO, bicicleta=None
    )
    
    with patch('routers.tranca.get_db') as mock_db, \
         patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
         patch('routers.tranca.TotemRepository') as mock_repo_totem:
        
        mock_repo_tranca_instance = MagicMock()
        mock_repo_tranca_instance.get_by_id.return_value = tranca_exemplo
        mock_repo_tranca_instance.get_totem_id.return_value = 1
        mock_repo_tranca_instance.update_status.return_value = tranca_retirada
        mock_repo_tranca_instance.desassociar_totem.return_value = True
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        mock_repo_totem_instance = MagicMock()
        mock_repo_totem_instance.get_by_id.return_value = totem_exemplo
        mock_repo_totem.return_value = mock_repo_totem_instance
        
        request_data = {
            "idTotem": 1,
            "idTranca": 1,
            "idFuncionario": 1,
            "statusAcaoReparador": "em_reparo"  # lowercase
        }
        
        response = client.post("/tranca/retirarDaRede", json=request_data)
        
        assert response.status_code == 200
