"""
Testes de integração para os endpoints do servico-equipamento.
Replica os cenários do Postman Collection com mocks dos serviços externos
(servico-aluguel e servico-externo).

Baseado no arquivo: ES2 Testes Postman - Amostra.postman_collection.json
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import httpx

from main import app
from models.bicicleta_model import Bicicleta, NovaBicicleta, StatusBicicleta
from models.tranca_model import Tranca, NovaTranca, StatusTranca
from models.totem_model import Totem


client = TestClient(app)


# ==============================================================================
# FIXTURES - Dados conforme Postman Collection
# ==============================================================================

@pytest.fixture
def dados_postman_bicicletas():
    """Bicicletas conforme dados iniciais do Postman"""
    return [
        Bicicleta(id=1, marca="Caloi", modelo="Caloi", ano="2020", numero=12345, status=StatusBicicleta.DISPONIVEL),
        Bicicleta(id=2, marca="Caloi", modelo="Caloi", ano="2020", numero=12345, status=StatusBicicleta.REPARO_SOLICITADO),
        Bicicleta(id=3, marca="Caloi", modelo="Caloi", ano="2020", numero=12345, status=StatusBicicleta.EM_USO),
        Bicicleta(id=4, marca="Caloi", modelo="Caloi", ano="2020", numero=12345, status=StatusBicicleta.EM_REPARO),
        Bicicleta(id=5, marca="Caloi", modelo="Caloi", ano="2020", numero=12345, status=StatusBicicleta.DISPONIVEL),
    ]


@pytest.fixture
def dados_postman_trancas():
    """Trancas conforme dados iniciais do Postman"""
    return [
        Tranca(id=1, numero=12345, localizacao="Rio de Janeiro", anoDeFabricacao="2020", 
               modelo="Caloi", status=StatusTranca.OCUPADA, bicicleta=1, totem=1),
        Tranca(id=2, numero=12345, localizacao="Rio de Janeiro", anoDeFabricacao="2020",
               modelo="Caloi", status=StatusTranca.LIVRE, bicicleta=None, totem=1),
        Tranca(id=3, numero=12345, localizacao="Rio de Janeiro", anoDeFabricacao="2020",
               modelo="Caloi", status=StatusTranca.OCUPADA, bicicleta=2, totem=1),
        Tranca(id=4, numero=12345, localizacao="Rio de Janeiro", anoDeFabricacao="2020",
               modelo="Caloi", status=StatusTranca.OCUPADA, bicicleta=5, totem=1),
        Tranca(id=5, numero=12345, localizacao="Rio de Janeiro", anoDeFabricacao="2020",
               modelo="Caloi", status=StatusTranca.EM_REPARO, bicicleta=None, totem=None),
        Tranca(id=6, numero=12345, localizacao="Rio de Janeiro", anoDeFabricacao="2020",
               modelo="Caloi", status=StatusTranca.REPARO_SOLICITADO, bicicleta=None, totem=1),
    ]


@pytest.fixture
def dados_postman_totem():
    """Totem conforme dados iniciais do Postman"""
    return Totem(id=1, localizacao="Rio de Janeiro")


@pytest.fixture
def mock_funcionario_response():
    """Resposta mockada do serviço de aluguel para funcionário"""
    return {
        "id": 1,
        "matricula": "12345",
        "email": "employee@example.com",
        "nome": "Beltrano",
        "idade": 25,
        "funcao": "Reparador",
        "cpf": "99999999999"
    }


@pytest.fixture
def mock_email_response():
    """Resposta mockada do serviço externo para envio de email"""
    return {
        "id": 1,
        "email": "employee@example.com",
        "assunto": "Operação realizada",
        "mensagem": "Detalhes da operação",
        "status": "ENVIADO"
    }


# ==============================================================================
# TESTES DE INTEGRAÇÃO - Cenário Postman: "Cadastrar bicicleta"
# ==============================================================================

class TestCadastrarBicicletaIntegracao:
    """
    Testes baseados no cenário Postman: "Cadastrar bicicleta"
    
    Pré-requisito: N/A
    Esperado: Status 200/201 com dados da bicicleta cadastrada
    """
    
    def test_cadastrar_bicicleta_sucesso_postman(self):
        """
        Replica exatamente o teste do Postman:
        - POST /bicicleta com payload específico
        - Verifica status 200/201
        - Verifica campos retornados
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo:
            
            mock_repo_instance = Mock()
            mock_repo.return_value = mock_repo_instance
            mock_repo_instance.get_all.return_value = []
            
            # Payload exato do Postman
            nova_bicicleta_payload = {
                "marca": "Nova Marca",
                "modelo": "Novo Modelo",
                "ano": "2020",
                "numero": 12345,
                "status": "NOVA"
            }
            
            # Mock retorna bicicleta criada com novo ID
            mock_repo_instance.create.return_value = Bicicleta(
                id=6,  # Novo ID (após os 5 existentes)
                marca=nova_bicicleta_payload["marca"],
                modelo=nova_bicicleta_payload["modelo"],
                ano=nova_bicicleta_payload["ano"],
                numero=nova_bicicleta_payload["numero"],
                status=StatusBicicleta.NOVA
            )
            
            response = client.post("/bicicleta", json=nova_bicicleta_payload)
            
            # Verificações do Postman:
            # pm.expect(pm.response.code).to.be.within(200, 201)
            assert response.status_code in [200, 201]
            
            json_response = response.json()
            
            # pm.expect(json.id).to.exist
            assert "id" in json_response
            assert json_response["id"] is not None
            
            # pm.expect(json.marca).to.equals(reqBody.marca)
            assert json_response["marca"] == nova_bicicleta_payload["marca"]
            
            # pm.expect(json.modelo).to.equals(reqBody.modelo)
            assert json_response["modelo"] == nova_bicicleta_payload["modelo"]
            
            # pm.expect(json.ano).to.equals(reqBody.ano)
            assert json_response["ano"] == nova_bicicleta_payload["ano"]
            
            # pm.expect(json.numero).to.equals(reqBody.numero)
            assert json_response["numero"] == nova_bicicleta_payload["numero"]
            
            # pm.expect(json.status).to.equals(reqBody.status)
            assert json_response["status"] == nova_bicicleta_payload["status"]
    
    def test_recuperar_bicicleta_cadastrada(self):
        """
        Segunda verificação do Postman: GET /bicicleta/{id} após cadastro
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo:
            
            mock_repo_instance = Mock()
            mock_repo.return_value = mock_repo_instance
            
            bicicleta_cadastrada = Bicicleta(
                id=6,
                marca="Nova Marca",
                modelo="Novo Modelo",
                ano="2020",
                numero=12345,
                status=StatusBicicleta.NOVA
            )
            mock_repo_instance.get_by_id.return_value = bicicleta_cadastrada
            
            response = client.get("/bicicleta/6")
            
            # pm.expect(response.status).equals(200)
            assert response.status_code == 200
            
            json_response = response.json()
            
            # pm.expect(json.id).to.equals(id)
            assert json_response["id"] == 6
            
            # Verifica demais campos
            assert json_response["marca"] == "Nova Marca"
            assert json_response["modelo"] == "Novo Modelo"
            assert json_response["status"] == "NOVA"


# ==============================================================================
# TESTES DE INTEGRAÇÃO - Endpoint /restaurarDados
# ==============================================================================

class TestRestaurarDadosIntegracao:
    """
    Testes do endpoint /restaurarDados
    
    Conforme Postman: Antes de cada teste, /restaurarDados é chamado
    para resetar o banco de dados
    """
    
    def test_restaurar_dados_sucesso(self):
        """
        GET /restaurarDados deve retornar 200 e resetar banco
        """
        response = client.get("/restaurarDados")
        
        assert response.status_code == 200
        assert "restaurado" in response.json()["mensagem"].lower()


# ==============================================================================
# TESTES DE INTEGRAÇÃO COM SERVIÇOS EXTERNOS MOCKADOS
# ==============================================================================

class TestIntegrarBicicletaNaRedeComServicosExternos:
    """
    Testes de integração de bicicleta na rede com serviços externos mockados.
    
    Cenário: integrarNaRede chama:
    1. servico-aluguel para validar funcionário
    2. servico-externo para enviar email de notificação
    """
    
    def test_integrar_bicicleta_com_funcionario_valido_e_email_enviado(
        self, mock_funcionario_response, mock_email_response
    ):
        """
        Cenário sucesso completo:
        - Funcionário encontrado no servico-aluguel
        - Email enviado com sucesso no servico-externo
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            # Setup repositórios
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            # Bicicleta NOVA (pode ser integrada)
            bicicleta_nova = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023", 
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
            
            # Tranca LIVRE (pode receber bicicleta)
            tranca_livre = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
            
            # Mock serviço de aluguel - funcionário válido
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            
            # Mock serviço de email - sucesso
            mock_email.notificar_inclusao_bicicleta.return_value = (True, mock_email_response)
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            assert response.status_code == 200
            assert "integrada na rede com sucesso" in response.json()["mensagem"]
            
            # Verifica que serviços externos foram chamados
            mock_aluguel.validar_funcionario.assert_called_once_with(1)
            mock_email.notificar_inclusao_bicicleta.assert_called_once()
    
    def test_integrar_bicicleta_funcionario_nao_encontrado_continua_operacao(self):
        """
        Cenário: Funcionário não encontrado no servico-aluguel
        A operação continua (warning é logado mas não bloqueia)
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta_nova = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
            
            tranca_livre = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
            
            # Mock serviço de aluguel - funcionário NÃO encontrado
            mock_aluguel.validar_funcionario.return_value = (False, None)
            
            # Mock serviço de email - sucesso
            mock_email.notificar_inclusao_bicicleta.return_value = (True, {})
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 999  # ID inexistente
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            # Operação deve continuar mesmo sem validar funcionário
            assert response.status_code == 200
            assert "integrada na rede com sucesso" in response.json()["mensagem"]
    
    def test_integrar_bicicleta_servico_aluguel_timeout(self):
        """
        Cenário: Timeout ao conectar com servico-aluguel
        A operação continua (serviço não é bloqueante)
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta_nova = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
            
            tranca_livre = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
            
            # Mock serviço de aluguel - simula timeout (retorna False)
            mock_aluguel.validar_funcionario.return_value = (False, None)
            
            mock_email.notificar_inclusao_bicicleta.return_value = (True, {})
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            # Operação continua mesmo com timeout
            assert response.status_code == 200
    
    def test_integrar_bicicleta_falha_envio_email(self):
        """
        Cenário: Falha ao enviar email via servico-externo
        A operação é concluída (email é notificação, não bloqueante)
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta_nova = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta_nova
            
            tranca_livre = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_livre
            
            mock_aluguel.validar_funcionario.return_value = (True, "email@test.com")
            
            # Mock serviço de email - FALHA
            mock_email.notificar_inclusao_bicicleta.return_value = (False, {"error": "Timeout"})
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            # Operação é concluída mesmo com falha de email
            assert response.status_code == 200
            assert "integrada na rede com sucesso" in response.json()["mensagem"]


class TestRetirarBicicletaDaRedeComServicosExternos:
    """
    Testes de retirada de bicicleta da rede com serviços externos mockados.
    """
    
    def test_retirar_bicicleta_para_reparo_sucesso_completo(
        self, mock_funcionario_response, mock_email_response
    ):
        """
        Cenário sucesso: Retira bicicleta para reparo
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.DISPONIVEL
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta
            
            tranca_ocupada = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.OCUPADA, bicicleta=1
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
            
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            mock_email.notificar_retirada_bicicleta.return_value = (True, mock_email_response)
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1,
                "statusAcaoReparador": "EM_REPARO"
            }
            
            response = client.post("/bicicleta/retirarDaRede", json=request_data)
            
            assert response.status_code == 200
            assert "retirada da rede com sucesso" in response.json()["mensagem"]
            assert response.json()["novoStatus"] == "EM_REPARO"
            
            mock_aluguel.validar_funcionario.assert_called_once_with(1)
            mock_email.notificar_retirada_bicicleta.assert_called_once()
    
    def test_retirar_bicicleta_para_aposentadoria(self):
        """
        Cenário: Retira bicicleta para aposentadoria
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.REPARO_SOLICITADO
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta
            
            tranca_ocupada = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.OCUPADA, bicicleta=1
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_ocupada
            
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            mock_email.notificar_retirada_bicicleta.return_value = (True, {})
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1,
                "statusAcaoReparador": "APOSENTADA"
            }
            
            response = client.post("/bicicleta/retirarDaRede", json=request_data)
            
            assert response.status_code == 200
            assert response.json()["novoStatus"] == "APOSENTADA"


class TestIntegrarTrancaNaRedeComServicosExternos:
    """
    Testes de integração de tranca na rede com serviços externos mockados.
    """
    
    def test_integrar_tranca_sucesso_completo(
        self, mock_funcionario_response, mock_email_response, dados_postman_totem
    ):
        """
        Cenário sucesso: Integra tranca NOVA na rede
        """
        with patch('routers.tranca.get_db'), \
             patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
             patch('routers.tranca.TotemRepository') as mock_repo_totem, \
             patch('routers.tranca.aluguel_service') as mock_aluguel, \
             patch('routers.tranca.email_service') as mock_email:
            
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            mock_repo_totem_instance = Mock()
            mock_repo_totem.return_value = mock_repo_totem_instance
            
            tranca_nova = Tranca(
                id=5, numero=12345, localizacao="Rio de Janeiro",
                anoDeFabricacao="2020", modelo="Caloi", 
                status=StatusTranca.NOVA, bicicleta=None, totem=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_nova
            mock_repo_totem_instance.get_by_id.return_value = dados_postman_totem
            
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            mock_email.notificar_inclusao_tranca.return_value = (True, mock_email_response)
            
            request_data = {
                "idTotem": 1,
                "idTranca": 5,
                "idFuncionario": 1
            }
            
            response = client.post("/tranca/integrarNaRede", json=request_data)
            
            assert response.status_code == 200
            assert "integrada na rede com sucesso" in response.json()["mensagem"]
            
            mock_aluguel.validar_funcionario.assert_called_once_with(1)
            mock_email.notificar_inclusao_tranca.assert_called_once()
    
    def test_integrar_tranca_retornando_de_reparo(
        self, mock_funcionario_response, dados_postman_totem
    ):
        """
        Cenário: Integra tranca retornando de reparo (EM_REPARO -> LIVRE)
        """
        with patch('routers.tranca.get_db'), \
             patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
             patch('routers.tranca.TotemRepository') as mock_repo_totem, \
             patch('routers.tranca.aluguel_service') as mock_aluguel, \
             patch('routers.tranca.email_service') as mock_email:
            
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            mock_repo_totem_instance = Mock()
            mock_repo_totem.return_value = mock_repo_totem_instance
            
            tranca_em_reparo = Tranca(
                id=5, numero=12345, localizacao="Rio de Janeiro",
                anoDeFabricacao="2020", modelo="Caloi",
                status=StatusTranca.EM_REPARO, bicicleta=None, totem=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_em_reparo
            mock_repo_totem_instance.get_by_id.return_value = dados_postman_totem
            
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            mock_email.notificar_inclusao_tranca.return_value = (True, {})
            
            request_data = {
                "idTotem": 1,
                "idTranca": 5,
                "idFuncionario": 1
            }
            
            response = client.post("/tranca/integrarNaRede", json=request_data)
            
            assert response.status_code == 200


class TestRetirarTrancaDaRedeComServicosExternos:
    """
    Testes de retirada de tranca da rede com serviços externos mockados.
    """
    
    def test_retirar_tranca_para_reparo_sucesso(
        self, mock_funcionario_response, mock_email_response
    ):
        """
        Cenário sucesso: Retira tranca para reparo
        """
        with patch('routers.tranca.get_db'), \
             patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
             patch('routers.tranca.TotemRepository') as mock_repo_totem, \
             patch('routers.tranca.aluguel_service') as mock_aluguel, \
             patch('routers.tranca.email_service') as mock_email:
            
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            mock_repo_totem_instance = Mock()
            mock_repo_totem.return_value = mock_repo_totem_instance
            
            # Tranca LIVRE (sem bicicleta) pode ser retirada
            tranca = Tranca(
                id=2, numero=12345, localizacao="Rio de Janeiro",
                anoDeFabricacao="2020", modelo="Caloi",
                status=StatusTranca.LIVRE, bicicleta=None, totem=1
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca
            mock_repo_tranca_instance.get_totem_id.return_value = 1
            
            totem = Totem(id=1, localizacao="Rio de Janeiro")
            mock_repo_totem_instance.get_by_id.return_value = totem
            
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            mock_email.notificar_retirada_tranca.return_value = (True, mock_email_response)
            
            request_data = {
                "idTotem": 1,
                "idTranca": 2,
                "idFuncionario": 1,
                "statusAcaoReparador": "EM_REPARO"
            }
            
            response = client.post("/tranca/retirarDaRede", json=request_data)
            
            assert response.status_code == 200
            assert "retirada da rede com sucesso" in response.json()["mensagem"]
            assert response.json()["novoStatus"] == "EM_REPARO"
    
    def test_retirar_tranca_com_bicicleta_deve_falhar(self):
        """
        Cenário erro: Tentar retirar tranca que possui bicicleta
        """
        with patch('routers.tranca.get_db'), \
             patch('routers.tranca.TrancaRepository') as mock_repo_tranca, \
             patch('routers.tranca.TotemRepository') as mock_repo_totem, \
             patch('routers.tranca.aluguel_service') as mock_aluguel, \
             patch('routers.tranca.email_service'):
            
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            mock_repo_totem_instance = Mock()
            mock_repo_totem.return_value = mock_repo_totem_instance
            
            # Tranca com bicicleta - não pode ser retirada
            tranca_com_bicicleta = Tranca(
                id=1, numero=12345, localizacao="Rio de Janeiro",
                anoDeFabricacao="2020", modelo="Caloi",
                status=StatusTranca.OCUPADA, bicicleta=1, totem=1
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca_com_bicicleta
            mock_repo_tranca_instance.get_totem_id.return_value = 1
            
            totem = Totem(id=1, localizacao="Rio de Janeiro")
            mock_repo_totem_instance.get_by_id.return_value = totem
            
            mock_aluguel.validar_funcionario.return_value = (True, "employee@example.com")
            
            request_data = {
                "idTotem": 1,
                "idTranca": 1,
                "idFuncionario": 1,
                "statusAcaoReparador": "EM_REPARO"
            }
            
            response = client.post("/tranca/retirarDaRede", json=request_data)
            
            assert response.status_code == 422
            assert "TRANCA_COM_BICICLETA" in str(response.json())


# ==============================================================================
# TESTES DE CENÁRIOS DE ERRO - Serviços Externos
# ==============================================================================

class TestCenariosErroServicosExternos:
    """
    Testes de cenários de erro com serviços externos.
    """
    
    def test_servico_aluguel_retorna_404(self):
        """
        Cenário: Serviço de aluguel retorna 404 para funcionário
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta
            
            tranca = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca
            
            # Serviço retorna funcionário não encontrado (404)
            mock_aluguel.validar_funcionario.return_value = (False, None)
            mock_email.notificar_inclusao_bicicleta.return_value = (True, {})
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 999
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            # Operação continua mesmo sem funcionário válido
            assert response.status_code == 200
    
    def test_servico_externo_retorna_500(self):
        """
        Cenário: Serviço externo retorna erro 500 ao enviar email
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta
            
            tranca = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca
            
            mock_aluguel.validar_funcionario.return_value = (True, "email@test.com")
            
            # Serviço externo retorna erro 500
            mock_email.notificar_inclusao_bicicleta.return_value = (
                False, 
                {"status_code": 500, "detail": "Internal Server Error"}
            )
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            # Operação é concluída mesmo com erro no serviço externo
            assert response.status_code == 200
    
    def test_servico_externo_connection_refused(self):
        """
        Cenário: Conexão recusada ao serviço externo
        """
        with patch('routers.bicicleta.get_db'), \
             patch('routers.bicicleta.BicicletaRepository') as mock_repo_bici, \
             patch('routers.bicicleta.TrancaRepository') as mock_repo_tranca, \
             patch('routers.bicicleta.aluguel_service') as mock_aluguel, \
             patch('routers.bicicleta.email_service') as mock_email:
            
            mock_repo_bici_instance = Mock()
            mock_repo_bici.return_value = mock_repo_bici_instance
            mock_repo_tranca_instance = Mock()
            mock_repo_tranca.return_value = mock_repo_tranca_instance
            
            bicicleta = Bicicleta(
                id=1, marca="Caloi", modelo="X", ano="2023",
                numero=100, status=StatusBicicleta.NOVA
            )
            mock_repo_bici_instance.get_by_id.return_value = bicicleta
            
            tranca = Tranca(
                id=1, numero=1, localizacao="ZS", anoDeFabricacao="2023",
                modelo="A", status=StatusTranca.LIVRE, bicicleta=None
            )
            mock_repo_tranca_instance.get_by_id.return_value = tranca
            
            mock_aluguel.validar_funcionario.return_value = (True, "email@test.com")
            
            # Simula conexão recusada
            mock_email.notificar_inclusao_bicicleta.return_value = (
                False,
                {"error": "Erro de conexão com serviço de email"}
            )
            
            request_data = {
                "idTranca": 1,
                "idBicicleta": 1,
                "idFuncionario": 1
            }
            
            response = client.post("/bicicleta/integrarNaRede", json=request_data)
            
            # Operação é concluída mesmo com falha de conexão
            assert response.status_code == 200


# ==============================================================================
# TESTES UNITÁRIOS DOS SERVICES (email_service e aluguel_service)
# ==============================================================================

class TestEmailServiceUnit:
    """
    Testes unitários do EmailService com httpx mockado.
    """
    
    def test_enviar_email_sucesso(self):
        """Testa envio de email com sucesso"""
        from services.email_service import EmailService
        
        with patch('services.email_service.httpx.Client') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "ENVIADO"}
            
            mock_client_instance = Mock()
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = EmailService(base_url="http://test:8002")
            sucesso, resposta = service.enviar_email(
                destinatario="test@email.com",
                assunto="Teste",
                mensagem="Mensagem de teste"
            )
            
            assert sucesso is True
            assert resposta["status"] == "ENVIADO"
    
    def test_enviar_email_timeout(self):
        """Testa timeout ao enviar email"""
        from services.email_service import EmailService
        
        with patch('services.email_service.httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = EmailService(base_url="http://test:8002")
            sucesso, resposta = service.enviar_email(
                destinatario="test@email.com",
                assunto="Teste",
                mensagem="Mensagem de teste"
            )
            
            assert sucesso is False
            assert "Timeout" in resposta["error"]
    
    def test_enviar_email_connection_error(self):
        """Testa erro de conexão ao enviar email"""
        from services.email_service import EmailService
        
        with patch('services.email_service.httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.side_effect = httpx.ConnectError("Connection refused")
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = EmailService(base_url="http://test:8002")
            sucesso, resposta = service.enviar_email(
                destinatario="test@email.com",
                assunto="Teste",
                mensagem="Mensagem de teste"
            )
            
            assert sucesso is False
            assert "conexão" in resposta["error"].lower()


class TestAluguelServiceUnit:
    """
    Testes unitários do AluguelService com httpx mockado.
    """
    
    def test_obter_funcionario_sucesso(self):
        """Testa obtenção de funcionário com sucesso"""
        from services.aluguel_service import AluguelService
        
        with patch('services.aluguel_service.httpx.Client') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": 1,
                "nome": "Beltrano",
                "email": "employee@example.com"
            }
            
            mock_client_instance = Mock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = AluguelService(base_url="http://test:8001")
            sucesso, dados = service.obter_funcionario(1)
            
            assert sucesso is True
            assert dados["nome"] == "Beltrano"
            assert dados["email"] == "employee@example.com"
    
    def test_obter_funcionario_nao_encontrado(self):
        """Testa funcionário não encontrado (404)"""
        from services.aluguel_service import AluguelService
        
        with patch('services.aluguel_service.httpx.Client') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            
            mock_client_instance = Mock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = AluguelService(base_url="http://test:8001")
            sucesso, dados = service.obter_funcionario(999)
            
            assert sucesso is False
            assert dados["status_code"] == 404
    
    def test_validar_funcionario_retorna_email(self):
        """Testa validação de funcionário retornando email"""
        from services.aluguel_service import AluguelService
        
        with patch('services.aluguel_service.httpx.Client') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": 1,
                "nome": "Beltrano",
                "email": "employee@example.com"
            }
            
            mock_client_instance = Mock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = AluguelService(base_url="http://test:8001")
            valido, email = service.validar_funcionario(1)
            
            assert valido is True
            assert email == "employee@example.com"
    
    def test_obter_ciclista_sucesso(self):
        """Testa obtenção de ciclista com sucesso"""
        from services.aluguel_service import AluguelService
        
        with patch('services.aluguel_service.httpx.Client') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": 1,
                "nome": "Fulano Beltrano",
                "email": "user@example.com",
                "status": "CONFIRMADO"
            }
            
            mock_client_instance = Mock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__enter__ = Mock(return_value=mock_client_instance)
            mock_client.return_value.__exit__ = Mock(return_value=False)
            
            service = AluguelService(base_url="http://test:8001")
            sucesso, dados = service.obter_ciclista(1)
            
            assert sucesso is True
            assert dados["nome"] == "Fulano Beltrano"
            assert dados["status"] == "CONFIRMADO"
