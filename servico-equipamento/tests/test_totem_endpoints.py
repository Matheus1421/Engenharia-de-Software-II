"""
Testes unitários para os endpoints de totens.
Cobre todos os cenários de sucesso e erro dos endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app
from models.totem_model import Totem, NovoTotem
from models.tranca_model import Tranca, StatusTranca
from models.bicicleta_model import Bicicleta, StatusBicicleta


client = TestClient(app)


# FIXTURES 

@pytest.fixture
def totem_exemplo():
    """Totem de exemplo para testes"""
    return Totem(
        id=1,
        localizacao="Zona Sul - Copacabana",
        descricao="Totem principal da Zona Sul"
    )


@pytest.fixture
def totem_exemplo_2():
    """Segundo totem de exemplo"""
    return Totem(
        id=2,
        localizacao="Zona Norte - Tijuca",
        descricao="Totem da Tijuca"
    )


@pytest.fixture
def novo_totem_valido():
    """Dados válidos para criar novo totem"""
    return {
        "localizacao": "Centro - Praça XV",
        "descricao": "Totem do Centro Histórico"
    }


@pytest.fixture
def tranca_exemplo():
    """Tranca associada a um totem"""
    return Tranca(
        id=1,
        numero=1,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.LIVRE,
        bicicleta=None
    )


@pytest.fixture
def tranca_com_bicicleta():
    """Tranca ocupada com bicicleta"""
    return Tranca(
        id=2,
        numero=2,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.OCUPADA,
        bicicleta=1
    )


@pytest.fixture
def bicicleta_exemplo():
    """Bicicleta de exemplo"""
    return Bicicleta(
        id=1,
        marca="Caloi",
        modelo="Mountain Bike",
        ano="2023",
        numero=100,
        status=StatusBicicleta.DISPONIVEL
    )


# TESTES GET /totem 

def test_listar_totems_sucesso(totem_exemplo, totem_exemplo_2):
    """Testa listagem de todos os totems - sucesso"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = [totem_exemplo, totem_exemplo_2]
        
        response = client.get("/totem")
        
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["id"] == 1
        assert response.json()[0]["localizacao"] == "Zona Sul - Copacabana"
        assert response.json()[1]["id"] == 2
        mock_repo_instance.get_all.assert_called_once()


def test_listar_totems_lista_vazia():
    """Testa listagem quando não há totems cadastrados"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = []
        
        response = client.get("/totem")
        
        assert response.status_code == 200
        assert response.json() == []


def test_listar_totems_multiplos(totem_exemplo):
    """Testa listagem com múltiplos totems"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        
        totems = [
            Totem(id=i, localizacao=f"Localização {i}", descricao=f"Totem {i}")
            for i in range(1, 6)
        ]
        mock_repo_instance.get_all.return_value = totems
        
        response = client.get("/totem")
        
        assert response.status_code == 200
        assert len(response.json()) == 5


# TESTES POST /totem 

def test_cadastrar_totem_sucesso(novo_totem_valido):
    """Testa cadastro de novo totem - sucesso"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.create.return_value = Totem(
            id=1,
            localizacao=novo_totem_valido["localizacao"],
            descricao=novo_totem_valido["descricao"]
        )
        
        response = client.post("/totem", json=novo_totem_valido)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["localizacao"] == "Centro - Praça XV"
        assert response.json()["descricao"] == "Totem do Centro Histórico"
        mock_repo_instance.create.assert_called_once()


def test_cadastrar_totem_sem_descricao():
    """Testa cadastro de totem sem descrição (opcional)"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.create.return_value = Totem(
            id=1,
            localizacao="Zona Oeste - Barra",
            descricao=""
        )
        
        novo_totem = {
            "localizacao": "Zona Oeste - Barra"
        }
        
        response = client.post("/totem", json=novo_totem)
        
        assert response.status_code == 200
        assert response.json()["localizacao"] == "Zona Oeste - Barra"


def test_cadastrar_totem_localizacao_vazia():
    """Testa erro ao cadastrar totem com localização vazia"""
    novo_totem = {
        "localizacao": "",
        "descricao": "Descrição qualquer"
    }
    
    response = client.post("/totem", json=novo_totem)
    
    assert response.status_code == 422
    assert "LOCALIZACAO_INVALIDA" in str(response.json())


def test_cadastrar_totem_localizacao_apenas_espacos():
    """Testa erro ao cadastrar totem com localização contendo apenas espaços"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository'):
        
        novo_totem = {
            "localizacao": "   ",
            "descricao": "Descrição qualquer"
        }
        
        response = client.post("/totem", json=novo_totem)
        
        assert response.status_code == 422
        assert "LOCALIZACAO_INVALIDA" in str(response.json())


def test_cadastrar_totem_sem_localizacao():
    """Testa erro ao cadastrar totem sem campo localização"""
    novo_totem = {
        "descricao": "Descrição qualquer"
    }
    
    response = client.post("/totem", json=novo_totem)
    
    assert response.status_code == 422


def test_cadastrar_totem_exception_generica():
    """Testa tratamento de exceção genérica no cadastro"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.create.side_effect = Exception("Erro no banco")
        
        novo_totem = {
            "localizacao": "Centro",
            "descricao": "Teste"
        }
        
        response = client.post("/totem", json=novo_totem)
        
        assert response.status_code == 422
        assert "DADOS_INVALIDOS" in str(response.json())


# TESTES PUT /totem/{id} 

def test_editar_totem_sucesso(totem_exemplo):
    """Testa edição de totem - sucesso"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = totem_exemplo
        
        totem_atualizado = Totem(
            id=1,
            localizacao="Zona Sul - Ipanema",
            descricao="Totem atualizado"
        )
        mock_repo_instance.update.return_value = totem_atualizado
        
        dados_atualizacao = {
            "localizacao": "Zona Sul - Ipanema",
            "descricao": "Totem atualizado"
        }
        
        response = client.put("/totem/1", json=dados_atualizacao)
        
        assert response.status_code == 200
        assert response.json()["localizacao"] == "Zona Sul - Ipanema"
        assert response.json()["descricao"] == "Totem atualizado"
        mock_repo_instance.update.assert_called_once()


def test_editar_totem_nao_encontrado():
    """Testa erro ao editar totem inexistente"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        dados_atualizacao = {
            "localizacao": "Centro",
            "descricao": "Teste"
        }
        
        response = client.put("/totem/999", json=dados_atualizacao)
        
        assert response.status_code == 404
        assert "TOTEM_NAO_ENCONTRADO" in str(response.json())


def test_editar_totem_localizacao_vazia(totem_exemplo):
    """Testa erro ao editar totem com localização vazia"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = totem_exemplo
        
        dados_atualizacao = {
            "localizacao": "",
            "descricao": "Descrição"
        }
        
        response = client.put("/totem/1", json=dados_atualizacao)
        
        assert response.status_code == 422
        assert "LOCALIZACAO_INVALIDA" in str(response.json())


def test_editar_totem_localizacao_apenas_espacos(totem_exemplo):
    """Testa erro ao editar totem com localização contendo apenas espaços"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = totem_exemplo
        
        dados_atualizacao = {
            "localizacao": "   ",
            "descricao": "Descrição"
        }
        
        response = client.put("/totem/1", json=dados_atualizacao)
        
        assert response.status_code == 422
        assert "LOCALIZACAO_INVALIDA" in str(response.json())


def test_editar_totem_exception_generica(totem_exemplo):
    """Testa tratamento de exceção genérica na edição"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = totem_exemplo
        mock_repo_instance.update.side_effect = Exception("Erro no banco")
        
        dados_atualizacao = {
            "localizacao": "Centro",
            "descricao": "Teste"
        }
        
        response = client.put("/totem/1", json=dados_atualizacao)
        
        assert response.status_code == 422
        assert "DADOS_INVALIDOS" in str(response.json())


# TESTES DELETE /totem/{id} 

def test_remover_totem_sucesso(totem_exemplo):
    """Testa remoção de totem - sucesso"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = totem_exemplo
        mock_repo_instance.delete.return_value = True
        
        response = client.delete("/totem/1")
        
        assert response.status_code == 200
        assert "removido com sucesso" in response.json()["mensagem"]
        mock_repo_instance.delete.assert_called_once_with(1)


def test_remover_totem_nao_encontrado():
    """Testa erro ao remover totem inexistente"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.delete("/totem/999")
        
        assert response.status_code == 404
        assert "TOTEM_NAO_ENCONTRADO" in str(response.json())


def test_remover_totem_verifica_existencia_antes():
    """Testa que a verificação de existência é feita antes da remoção"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.delete("/totem/1")
        
        # Não deve chamar delete se o totem não existe
        mock_repo_instance.delete.assert_not_called()
        assert response.status_code == 404


# TESTES GET /totem/{id}/trancas 

def test_listar_trancas_do_totem_sucesso(totem_exemplo, tranca_exemplo):
    """Testa listagem de trancas de um totem - sucesso"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo:
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = [1]
        mock_tranca_instance.get_by_id.return_value = tranca_exemplo
        
        response = client.get("/totem/1/trancas")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 1
        assert response.json()[0]["numero"] == 1


def test_listar_trancas_do_totem_multiplas_trancas(totem_exemplo):
    """Testa listagem de totem com múltiplas trancas"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo:
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = [1, 2, 3]
        
        trancas = [
            Tranca(id=i, numero=i, localizacao="ZS", anoDeFabricacao="2023",
                   modelo="A", status=StatusTranca.LIVRE, bicicleta=None)
            for i in [1, 2, 3]
        ]
        
        mock_tranca_instance.get_by_id.side_effect = trancas
        
        response = client.get("/totem/1/trancas")
        
        assert response.status_code == 200
        assert len(response.json()) == 3


def test_listar_trancas_do_totem_sem_trancas(totem_exemplo):
    """Testa listagem de totem sem trancas associadas"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo:
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = []
        
        response = client.get("/totem/1/trancas")
        
        assert response.status_code == 200
        assert response.json() == []


def test_listar_trancas_totem_nao_encontrado():
    """Testa erro ao listar trancas de totem inexistente"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.get("/totem/999/trancas")
        
        assert response.status_code == 404
        assert "TOTEM_NAO_ENCONTRADO" in str(response.json())


def test_listar_trancas_id_invalido_zero():
    """Testa erro com ID zero"""
    response = client.get("/totem/0/trancas")
    
    assert response.status_code == 422
    assert "ID_INVALIDO" in str(response.json())


def test_listar_trancas_id_invalido_negativo():
    """Testa erro com ID negativo"""
    response = client.get("/totem/-1/trancas")
    
    assert response.status_code == 422
    assert "ID_INVALIDO" in str(response.json())


def test_listar_trancas_id_invalido_muito_negativo():
    """Testa erro com ID muito negativo"""
    response = client.get("/totem/-999/trancas")
    
    assert response.status_code == 422
    assert "ID_INVALIDO" in str(response.json())


# TESTES GET /totem/{id}/bicicletas 

def test_listar_bicicletas_do_totem_sucesso(totem_exemplo, tranca_com_bicicleta, bicicleta_exemplo):
    """Testa listagem de bicicletas de um totem - sucesso"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo, \
         patch('routers.totem.BicicletaRepository') as mock_bici_repo:
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        mock_bici_instance = Mock()
        mock_bici_repo.return_value = mock_bici_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = [2]
        mock_tranca_instance.get_by_id.return_value = tranca_com_bicicleta
        mock_bici_instance.get_by_id.return_value = bicicleta_exemplo
        
        response = client.get("/totem/1/bicicletas")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 1
        assert response.json()[0]["marca"] == "Caloi"


def test_listar_bicicletas_do_totem_sem_bicicletas(totem_exemplo, tranca_exemplo):
    """Testa listagem de totem sem bicicletas (trancas vazias)"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo, \
         patch('routers.totem.BicicletaRepository'):
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = [1]
        mock_tranca_instance.get_by_id.return_value = tranca_exemplo  # Sem bicicleta
        
        response = client.get("/totem/1/bicicletas")
        
        assert response.status_code == 200
        assert response.json() == []


def test_listar_bicicletas_do_totem_multiplas_bicicletas(totem_exemplo):
    """Testa listagem de totem com múltiplas bicicletas"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo, \
         patch('routers.totem.BicicletaRepository') as mock_bici_repo:
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        mock_bici_instance = Mock()
        mock_bici_repo.return_value = mock_bici_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = [1, 2, 3]
        
        # Trancas com bicicletas diferentes
        trancas = [
            Tranca(id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                   modelo="A", status=StatusTranca.OCUPADA, bicicleta=10),
            Tranca(id=2, numero=2, localizacao="ZS", anoDeFabricacao="2023",
                   modelo="A", status=StatusTranca.OCUPADA, bicicleta=20),
            Tranca(id=3, numero=3, localizacao="ZS", anoDeFabricacao="2023",
                   modelo="A", status=StatusTranca.LIVRE, bicicleta=None),
        ]
        
        bicicletas = [
            Bicicleta(id=10, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL),
            Bicicleta(id=20, marca="Trek", modelo="Y", ano="2023", numero=200, status=StatusBicicleta.DISPONIVEL),
        ]
        
        mock_tranca_instance.get_by_id.side_effect = trancas
        mock_bici_instance.get_by_id.side_effect = bicicletas
        
        response = client.get("/totem/1/bicicletas")
        
        assert response.status_code == 200
        assert len(response.json()) == 2


def test_listar_bicicletas_totem_nao_encontrado():
    """Testa erro ao listar bicicletas de totem inexistente"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.get("/totem/999/bicicletas")
        
        assert response.status_code == 404
        assert "TOTEM_NAO_ENCONTRADO" in str(response.json())


def test_listar_bicicletas_id_invalido_zero():
    """Testa erro com ID zero"""
    response = client.get("/totem/0/bicicletas")
    
    assert response.status_code == 422
    assert "ID_INVALIDO" in str(response.json())


def test_listar_bicicletas_id_invalido_negativo():
    """Testa erro com ID negativo"""
    response = client.get("/totem/-5/bicicletas")
    
    assert response.status_code == 422
    assert "ID_INVALIDO" in str(response.json())


def test_listar_bicicletas_sem_duplicatas(totem_exemplo):
    """Testa que não retorna bicicletas duplicadas"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository') as mock_tranca_repo, \
         patch('routers.totem.BicicletaRepository') as mock_bici_repo:
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        mock_tranca_instance = Mock()
        mock_tranca_repo.return_value = mock_tranca_instance
        mock_bici_instance = Mock()
        mock_bici_repo.return_value = mock_bici_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = [1, 2]
        
        # Ambas trancas com a mesma bicicleta (cenário de teste)
        tranca_1 = Tranca(id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                         modelo="A", status=StatusTranca.OCUPADA, bicicleta=10)
        tranca_2 = Tranca(id=2, numero=2, localizacao="ZS", anoDeFabricacao="2023",
                         modelo="A", status=StatusTranca.OCUPADA, bicicleta=10)
        
        bicicleta = Bicicleta(id=10, marca="Caloi", modelo="X", ano="2023",
                             numero=100, status=StatusBicicleta.DISPONIVEL)
        
        mock_tranca_instance.get_by_id.side_effect = [tranca_1, tranca_2]
        mock_bici_instance.get_by_id.return_value = bicicleta
        
        response = client.get("/totem/1/bicicletas")
        
        # Deve retornar apenas uma bicicleta, mesmo que esteja em duas trancas
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == 10


def test_listar_bicicletas_totem_sem_trancas(totem_exemplo):
    """Testa listagem de bicicletas em totem sem trancas"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_totem_repo, \
         patch('routers.totem.TrancaRepository'), \
         patch('routers.totem.BicicletaRepository'):
        
        mock_totem_instance = Mock()
        mock_totem_repo.return_value = mock_totem_instance
        
        mock_totem_instance.get_by_id.return_value = totem_exemplo
        mock_totem_instance.get_trancas_ids.return_value = []
        
        response = client.get("/totem/1/bicicletas")
        
        assert response.status_code == 200
        assert response.json() == []



def test_listar_trancas_verifica_id_antes_de_buscar_totem():
    """Testa que validação de ID ocorre antes de buscar totem"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/totem/-1/trancas")
        
        # Não deve chamar get_by_id se o ID é inválido
        mock_repo_instance.get_by_id.assert_not_called()
        assert response.status_code == 422


def test_listar_bicicletas_verifica_id_antes_de_buscar_totem():
    """Testa que validação de ID ocorre antes de buscar totem"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        
        response = client.get("/totem/0/bicicletas")
        
        # Não deve chamar get_by_id se o ID é inválido
        mock_repo_instance.get_by_id.assert_not_called()
        assert response.status_code == 422


def test_cadastrar_totem_com_descricao_longa():
    """Testa cadastro de totem com descrição muito longa"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        
        descricao_longa = "X" * 1000
        mock_repo_instance.create.return_value = Totem(
            id=1,
            localizacao="Centro",
            descricao=descricao_longa
        )
        
        novo_totem = {
            "localizacao": "Centro",
            "descricao": descricao_longa
        }
        
        response = client.post("/totem", json=novo_totem)
        
        assert response.status_code == 200
        assert len(response.json()["descricao"]) == 1000


def test_editar_totem_campos_especiais():
    """Testa edição de totem com caracteres especiais na localização"""
    with patch('routers.totem.get_db'), \
         patch('routers.totem.TotemRepository') as mock_repo:
        
        totem_existente = Totem(id=1, localizacao="Centro", descricao="Teste")
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = totem_existente
        
        totem_atualizado = Totem(
            id=1,
            localizacao="Centro - Praça XV, nº 123",
            descricao="Descrição com acentuação: São João"
        )
        mock_repo_instance.update.return_value = totem_atualizado
        
        dados = {
            "localizacao": "Centro - Praça XV, nº 123",
            "descricao": "Descrição com acentuação: São João"
        }
        
        response = client.put("/totem/1", json=dados)
        
        assert response.status_code == 200
        assert "Praça XV" in response.json()["localizacao"]
        assert "São João" in response.json()["descricao"]
