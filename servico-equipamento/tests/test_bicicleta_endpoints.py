"""
Testes unitários para os endpoints de bicicletas.
Cobre todos os cenários de sucesso e erro dos endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock

from main import app
from models.bicicleta_model import Bicicleta, NovaBicicleta, StatusBicicleta
from models.tranca_model import Tranca, StatusTranca


client = TestClient(app)


#   FIXTURES  

@pytest.fixture
def mock_db():
    """Mock do banco de dados"""
    return MagicMock()


@pytest.fixture
def bicicleta_exemplo():
    """Bicicleta de exemplo para testes"""
    return Bicicleta(
        id=1,
        marca="Caloi",
        modelo="Mountain Bike",
        ano="2023",
        numero=100,
        status=StatusBicicleta.DISPONIVEL
    )


@pytest.fixture
def nova_bicicleta_valida():
    """Dados válidos para criar nova bicicleta"""
    return {
        "marca": "Caloi",
        "modelo": "Speed",
        "ano": "2024",
        "numero": 200
    }


@pytest.fixture
def tranca_livre():
    """Tranca livre de exemplo"""
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
def tranca_ocupada_com_bicicleta():
    """Tranca ocupada com bicicleta"""
    return Tranca(
        id=1,
        numero=1,
        localizacao="Zona Sul",
        anoDeFabricacao="2023",
        modelo="Modelo A",
        status=StatusTranca.OCUPADA,
        bicicleta=1
    )


#   TESTES GET /bicicleta  

def test_listar_bicicletas_sucesso():
    """Testa listagem de todas as bicicletas - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo: # aqui ele mocka o construtor do BicicletaRepository
        
        # Setup
        mock_repo_instance = Mock() # aqui ele cria a instância mockada que será retornada pelo construtor mockado
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = [ # aqui ele define o retorno do método get_all da instância mockada
            Bicicleta(id=1, marca="Caloi", modelo="Mountain", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL),
            Bicicleta(id=2, marca="Trek", modelo="Speed", ano="2024", numero=101, status=StatusBicicleta.EM_USO)
        ] 
        
        # Executa
        response = client.get("/bicicleta")
        
        # Verifica
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["id"] == 1
        assert response.json()[0]["marca"] == "Caloi"
        assert response.json()[1]["id"] == 2
        mock_repo_instance.get_all.assert_called_once()


def test_listar_bicicletas_lista_vazia():
    """Testa listagem quando não há bicicletas cadastradas"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = []
        
        response = client.get("/bicicleta")
        
        assert response.status_code == 200
        assert response.json() == []


#   TESTES POST /bicicleta  

def test_cadastrar_bicicleta_sucesso(nova_bicicleta_valida):
    """Testa cadastro de nova bicicleta - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = []
        mock_repo_instance.create.return_value = Bicicleta(
            id=1,
            marca=nova_bicicleta_valida["marca"],
            modelo=nova_bicicleta_valida["modelo"],
            ano=nova_bicicleta_valida["ano"],
            numero=nova_bicicleta_valida["numero"],
            status=StatusBicicleta.NOVA
        )
        
        response = client.post("/bicicleta", json=nova_bicicleta_valida)
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["marca"] == "Caloi"
        assert response.json()["numero"] == 200
        mock_repo_instance.create.assert_called_once()


def test_cadastrar_bicicleta_numero_duplicado():
    """Testa erro ao cadastrar bicicleta com número duplicado"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.return_value = [
            Bicicleta(id=1, marca="Outra", modelo="Outro", ano="2022", numero=200, status=StatusBicicleta.DISPONIVEL)
        ]
        
        nova_bicicleta = {
            "marca": "Caloi",
            "modelo": "Speed",
            "ano": "2024",
            "numero": 200  # Número duplicado
        }
        
        response = client.post("/bicicleta", json=nova_bicicleta)
        
        assert response.status_code == 422
        assert "NUMERO_DUPLICADO" in str(response.json())


def test_cadastrar_bicicleta_dados_invalidos():
    """Testa erro ao cadastrar bicicleta com dados inválidos"""
    bicicleta_invalida = {
        "marca": "",  # Marca vazia
        "modelo": "Speed",
        "ano": "2024",
        "numero": -1  # Número negativo
    }
    
    response = client.post("/bicicleta", json=bicicleta_invalida)
    
    assert response.status_code == 422


def test_cadastrar_bicicleta_campos_faltando():
    """Testa erro ao cadastrar bicicleta sem campos obrigatórios"""
    bicicleta_incompleta = {
        "marca": "Caloi"
        # Faltam outros campos
    }
    
    response = client.post("/bicicleta", json=bicicleta_incompleta)
    
    assert response.status_code == 422


#   TESTES GET /bicicleta/{id}  

def test_obter_bicicleta_sucesso(bicicleta_exemplo):
    """Testa obtenção de bicicleta por ID - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        
        response = client.get("/bicicleta/1")
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["marca"] == "Caloi"
        assert response.json()["numero"] == 100
        mock_repo_instance.get_by_id.assert_called_once_with(1)


def test_obter_bicicleta_nao_encontrada():
    """Testa erro ao buscar bicicleta inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.get("/bicicleta/999")
        
        assert response.status_code == 404
        assert "BICICLETA_NAO_ENCONTRADA" in str(response.json())


#   TESTES PUT /bicicleta/{id}  

def test_editar_bicicleta_sucesso(bicicleta_exemplo):
    """Testa edição de bicicleta - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_instance.get_all.return_value = [bicicleta_exemplo]
        
        bicicleta_atualizada = Bicicleta(
            id=1,
            marca="Caloi",
            modelo="Speed Atualizada",
            ano="2024",
            numero=100,
            status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_instance.update.return_value = bicicleta_atualizada
        
        dados_atualizacao = {
            "marca": "Caloi",
            "modelo": "Speed Atualizada",
            "ano": "2024",
            "numero": 100
        }
        
        response = client.put("/bicicleta/1", json=dados_atualizacao)
        
        assert response.status_code == 200
        assert response.json()["modelo"] == "Speed Atualizada"
        mock_repo_instance.update.assert_called_once()


def test_editar_bicicleta_nao_encontrada():
    """Testa erro ao editar bicicleta inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        dados_atualizacao = {
            "marca": "Caloi",
            "modelo": "Speed",
            "ano": "2024",
            "numero": 100
        }
        
        response = client.put("/bicicleta/999", json=dados_atualizacao)
        
        assert response.status_code == 404
        assert "BICICLETA_NAO_ENCONTRADA" in str(response.json())


def test_editar_bicicleta_numero_duplicado(bicicleta_exemplo):
    """Testa erro ao editar bicicleta com número já usado por outra"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_instance.get_all.return_value = [
            bicicleta_exemplo,
            Bicicleta(id=2, marca="Trek", modelo="X", ano="2023", numero=200, status=StatusBicicleta.DISPONIVEL)
        ]
        
        dados_atualizacao = {
            "marca": "Caloi",
            "modelo": "Speed",
            "ano": "2024",
            "numero": 200  # Número já usado por outra bicicleta
        }
        
        response = client.put("/bicicleta/1", json=dados_atualizacao)
        
        assert response.status_code == 422
        assert "NUMERO_DUPLICADO" in str(response.json())


#   TESTES DELETE /bicicleta/{id}  

def test_remover_bicicleta_sucesso():
    """Testa remoção de bicicleta - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.delete.return_value = True
        
        response = client.delete("/bicicleta/1")
        
        assert response.status_code == 200
        assert "removida com sucesso" in response.json()["mensagem"]
        mock_repo_instance.delete.assert_called_once_with(1)


def test_remover_bicicleta_nao_encontrada():
    """Testa erro ao remover bicicleta inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None  # Bicicleta não existe
        
        response = client.delete("/bicicleta/999")
        
        assert response.status_code == 404
        assert "BICICLETA_NAO_ENCONTRADA" in str(response.json())


#   TESTES POST /bicicleta/{id}/status/{acao}  

def test_alterar_status_bicicleta_sucesso(bicicleta_exemplo):
    """Testa alteração de status da bicicleta - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        
        bicicleta_atualizada = Bicicleta(
            id=1,
            marca="Caloi",
            modelo="Mountain Bike",
            ano="2023",
            numero=100,
            status=StatusBicicleta.EM_REPARO
        )
        mock_repo_instance.update_status.return_value = bicicleta_atualizada
        
        response = client.post("/bicicleta/1/status/EM_REPARO")
        
        assert response.status_code == 200
        assert response.json()["status"] == "EM_REPARO"
        mock_repo_instance.update_status.assert_called_once()


def test_alterar_status_bicicleta_todos_status_validos(bicicleta_exemplo):
    """Testa todos os status válidos"""
    status_validos = ["DISPONIVEL", "EM_USO", "NOVA", "APOSENTADA", "REPARO_SOLICITADO", "EM_REPARO"]
    
    for status in status_validos:
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo:
            
            mock_repo_instance = Mock()
            mock_repo.return_value = mock_repo_instance
            mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
            
            bicicleta_atualizada = Bicicleta(
                id=1,
                marca="Caloi",
                modelo="Mountain Bike",
                ano="2023",
                numero=100,
                status=StatusBicicleta[status]
            )
            mock_repo_instance.update_status.return_value = bicicleta_atualizada
            
            response = client.post(f"/bicicleta/1/status/{status}")
            
            assert response.status_code == 200
            assert response.json()["status"] == status


def test_alterar_status_bicicleta_status_invalido(bicicleta_exemplo):
    """Testa erro ao usar status inválido"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        
        response = client.post("/bicicleta/1/status/STATUS_INVALIDO")
        
        assert response.status_code == 422
        assert "STATUS_INVALIDO" in str(response.json())


def test_alterar_status_bicicleta_nao_encontrada():
    """Testa erro ao alterar status de bicicleta inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = None
        
        response = client.post("/bicicleta/999/status/EM_REPARO")
        
        assert response.status_code == 404
        assert "BICICLETA_NAO_ENCONTRADA" in str(response.json())


def test_alterar_status_case_insensitive(bicicleta_exemplo):
    """Testa que o status com Enum é case-sensitive (maiúsculas obrigatórias)"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        
        bicicleta_atualizada = Bicicleta(
            id=1,
            marca="Caloi",
            modelo="Mountain Bike",
            ano="2023",
            numero=100,
            status=StatusBicicleta.EM_REPARO
        )
        mock_repo_instance.update_status.return_value = bicicleta_atualizada
        
        # Com Enum, minúsculas não são aceitas - retorna 422
        response = client.post("/bicicleta/1/status/em_reparo")
        assert response.status_code == 422
        
        # Maiúsculas funcionam
        response = client.post("/bicicleta/1/status/EM_REPARO")
        assert response.status_code == 200
        assert response.json()["status"] == "EM_REPARO"


#   TESTES POST /bicicleta/integrarNaRede  

def test_integrar_bicicleta_na_rede_sucesso_status_nova(tranca_livre):
    """Testa integração de bicicleta NOVA na rede - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta_nova = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.NOVA
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
        mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10
        }
        
        response = client.post("/bicicleta/integrarNaRede", json=request_data)
        
        assert response.status_code == 200
        assert "integrada na rede com sucesso" in response.json()["mensagem"]
        assert response.json()["idBicicleta"] == 1
        assert response.json()["idTranca"] == 1
        assert response.json()["idFuncionario"] == 10
        
        # Verifica que os métodos corretos foram chamados
        mock_repo_bici_instance.update_status.assert_called_once_with(1, StatusBicicleta.DISPONIVEL)
        mock_repo_tranca_instance.associar_bicicleta.assert_called_once_with(1, 1)
        mock_repo_tranca_instance.update_status.assert_called_once_with(1, StatusTranca.OCUPADA)


def test_integrar_bicicleta_na_rede_sucesso_status_em_reparo(tranca_livre):
    """Testa integração de bicicleta EM_REPARO na rede - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta_reparo = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.EM_REPARO
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta_reparo
        mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10
        }
        
        response = client.post("/bicicleta/integrarNaRede", json=request_data)
        
        assert response.status_code == 200
        assert "integrada na rede com sucesso" in response.json()["mensagem"]


def test_integrar_bicicleta_nao_encontrada(tranca_livre):
    """Testa erro ao integrar bicicleta inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository'):
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_bici_instance.get_by_id.return_value = None
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 999,
            "idFuncionario": 10
        }
        
        response = client.post("/bicicleta/integrarNaRede", json=request_data)
        
        assert response.status_code == 404
        assert "BICICLETA_NAO_ENCONTRADA" in str(response.json())


def test_integrar_tranca_nao_encontrada():
    """Testa erro ao integrar com tranca inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta_nova = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.NOVA
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
        mock_repo_tranca_instance.get_by_id.return_value = None
        
        request_data = {
            "idTranca": 999,
            "idBicicleta": 1,
            "idFuncionario": 10
        }
        
        response = client.post("/bicicleta/integrarNaRede", json=request_data)
        
        assert response.status_code == 404
        assert "TRANCA_NAO_ENCONTRADA" in str(response.json())


def test_integrar_bicicleta_status_invalido(tranca_livre):
    """Testa erro ao integrar bicicleta com status inválido"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        # Bicicleta com status DISPONIVEL (não permitido para integração)
        bicicleta_disponivel = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta_disponivel
        mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10
        }
        
        response = client.post("/bicicleta/integrarNaRede", json=request_data)
        
        assert response.status_code == 422
        assert "STATUS_BICICLETA_INVALIDO" in str(response.json())


def test_integrar_tranca_ocupada():
    """Testa erro ao integrar em tranca ocupada"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta_nova = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.NOVA
        )
        tranca_ocupada = Tranca(
            id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
            modelo="A", status=StatusTranca.OCUPADA, bicicleta=5
        )
        
        mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10
        }
        
        response = client.post("/bicicleta/integrarNaRede", json=request_data)
        
        assert response.status_code == 422
        assert "STATUS_TRANCA_INVALIDO" in str(response.json())


#   TESTES POST /bicicleta/retirarDaRede  

def test_retirar_bicicleta_da_rede_para_reparo(tranca_ocupada_com_bicicleta):
    """Testa retirada de bicicleta da rede para reparo - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada_com_bicicleta
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 200
        assert "retirada da rede com sucesso" in response.json()["mensagem"]
        assert response.json()["novoStatus"] == "EM_REPARO"
        
        # Verifica chamadas
        mock_repo_bici_instance.update_status.assert_called_once_with(1, StatusBicicleta.EM_REPARO)
        mock_repo_tranca_instance.associar_bicicleta.assert_called_once_with(1, None)
        mock_repo_tranca_instance.update_status.assert_called_once_with(1, StatusTranca.LIVRE)


def test_retirar_bicicleta_da_rede_para_aposentar(tranca_ocupada_com_bicicleta):
    """Testa retirada de bicicleta da rede para aposentadoria - sucesso"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada_com_bicicleta
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10,
            "statusAcaoReparador": "APOSENTADA"
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 200
        assert response.json()["novoStatus"] == "APOSENTADA"
        mock_repo_bici_instance.update_status.assert_called_once_with(1, StatusBicicleta.APOSENTADA)


def test_retirar_bicicleta_nao_encontrada():
    """Testa erro ao retirar bicicleta inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_bici_instance.get_by_id.return_value = None
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 999,
            "idFuncionario": 10,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 404
        assert "BICICLETA_NAO_ENCONTRADA" in str(response.json())


def test_retirar_tranca_nao_encontrada():
    """Testa erro ao retirar de tranca inexistente"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta
        mock_repo_tranca_instance.get_by_id.return_value = None
        
        request_data = {
            "idTranca": 999,
            "idBicicleta": 1,
            "idFuncionario": 10,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 404
        assert "TRANCA_NAO_ENCONTRADA" in str(response.json())


def test_retirar_bicicleta_nao_esta_na_tranca():
    """Testa erro ao retirar bicicleta que não está na tranca informada"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        tranca_com_outra_bicicleta = Tranca(
            id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
            modelo="A", status=StatusTranca.OCUPADA, bicicleta=999  # Bicicleta diferente
        )
        
        mock_repo_bici_instance.get_by_id.return_value = bicicleta
        mock_repo_tranca_instance.get_by_id.return_value = tranca_com_outra_bicicleta
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10,
            "statusAcaoReparador": "EM_REPARO"
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 422
        assert "BICICLETA_NAO_ESTA_NA_TRANCA" in str(response.json())


def test_retirar_status_destino_invalido(tranca_ocupada_com_bicicleta):
    """Testa erro ao usar status de destino inválido"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada_com_bicicleta
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10,
            "statusAcaoReparador": "DISPONIVEL"  # Status não permitido para retirada
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 422
        assert "STATUS_DESTINO_INVALIDO" in str(response.json())


def test_retirar_status_case_insensitive(tranca_ocupada_com_bicicleta):
    """Testa que statusAcaoReparador aceita minúsculas"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
         patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca:
        
        mock_repo_bici_instance = Mock()
        mock_repo_bici.return_value = mock_repo_bici_instance
        mock_repo_tranca_instance = Mock()
        mock_repo_tranca.return_value = mock_repo_tranca_instance
        
        bicicleta = Bicicleta(
            id=1, marca="Caloi", modelo="X", ano="2023", numero=100, status=StatusBicicleta.DISPONIVEL
        )
        mock_repo_bici_instance.get_by_id.return_value = bicicleta
        mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada_com_bicicleta
        
        request_data = {
            "idTranca": 1,
            "idBicicleta": 1,
            "idFuncionario": 10,
            "statusAcaoReparador": "em_reparo"  # minúsculas
        }
        
        response = client.post("/bicicleta/retirarDaRede", json=request_data)
        
        assert response.status_code == 200
        assert response.json()["novoStatus"] == "EM_REPARO"


#   TESTES DE COBERTURA ADICIONAL  

def test_cadastrar_bicicleta_exception_generica():
    """Testa tratamento de exceção genérica no cadastro"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_all.side_effect = Exception("Erro no banco")
        
        nova_bicicleta = {
            "marca": "Caloi",
            "modelo": "Speed",
            "ano": "2024",
            "numero": 200
        }
        
        response = client.post("/bicicleta", json=nova_bicicleta)
        
        assert response.status_code == 422
        assert "DADOS_INVALIDOS" in str(response.json())


def test_editar_bicicleta_exception_generica(bicicleta_exemplo):
    """Testa tratamento de exceção genérica na edição"""
    with patch('routers.bicicleta.get_db'), \
         patch('routers.bicicleta.BicicletaRepository') as mock_repo:
        
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.get_by_id.return_value = bicicleta_exemplo
        mock_repo_instance.get_all.side_effect = Exception("Erro no banco")
        
        dados_atualizacao = {
            "marca": "Caloi",
            "modelo": "Speed",
            "ano": "2024",
            "numero": 100
        }
        
        response = client.put("/bicicleta/1", json=dados_atualizacao)
        
        assert response.status_code == 422
        assert "DADOS_INVALIDOS" in str(response.json())
