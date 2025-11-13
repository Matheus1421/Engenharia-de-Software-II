"""
Testes unitários dos endpoints de funcionário.
Cobre UC15 (Manter Cadastro de Funcionário) - CRUD completo.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app
from models.funcionario_model import Funcionario, FuncaoFuncionario

client = TestClient(app)


#   FIXTURES

@pytest.fixture
def funcionario_exemplo():
    """Funcionário ADMINISTRATIVO para testes"""
    return Funcionario(
        matricula="F001",
        nome="Admin Sistema",
        idade=35,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="admin@scb.com",
        senha="admin123"
    )


@pytest.fixture
def funcionario_reparador():
    """Funcionário REPARADOR para testes"""
    return Funcionario(
        matricula="F002",
        nome="João Reparador",
        idade=28,
        funcao=FuncaoFuncionario.REPARADOR,
        cpf="98765432100",
        email="joao.reparador@scb.com",
        senha="reparador123"
    )


@pytest.fixture
def dados_funcionario_valido():
    """Dados válidos para criar novo funcionário"""
    return {
        "nome": "Carlos Silva",
        "idade": 40,
        "funcao": "ADMINISTRATIVO",
        "cpf": "55566677788",
        "email": "carlos@scb.com",
        "senha": "carlos123",
        "confirmacaoSenha": "carlos123"
    }


#   TESTES GET /funcionario

def test_listar_funcionarios_sucesso(funcionario_exemplo, funcionario_reparador):
    """UC15 - Testa listagem de todos os funcionários"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.listar.return_value = [funcionario_exemplo, funcionario_reparador]

        response = client.get("/funcionario")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["matricula"] == "F001"
        assert data[1]["matricula"] == "F002"
        mock_instance.listar.assert_called_once()


def test_listar_funcionarios_lista_vazia():
    """UC15 - Testa listagem quando não há funcionários"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.listar.return_value = []

        response = client.get("/funcionario")

        assert response.status_code == 200
        assert response.json() == []


#   TESTES GET /funcionario/{matricula}

def test_buscar_funcionario_sucesso(funcionario_exemplo):
    """UC15 - Testa busca de funcionário por matrícula - sucesso"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_matricula.return_value = funcionario_exemplo

        response = client.get("/funcionario/F001")

        assert response.status_code == 200
        data = response.json()
        assert data["matricula"] == "F001"
        assert data["nome"] == "Admin Sistema"
        assert data["funcao"] == "ADMINISTRATIVO"
        mock_instance.buscar_por_matricula.assert_called_once_with("F001")


def test_buscar_funcionario_nao_encontrado():
    """UC15 - Testa erro ao buscar funcionário inexistente"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_matricula.return_value = None

        response = client.get("/funcionario/F999")

        assert response.status_code == 404


#   TESTES POST /funcionario

def test_cadastrar_funcionario_sucesso(dados_funcionario_valido):
    """UC15 - Testa cadastro de novo funcionário - sucesso"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance

        # Funcionário criado com matrícula F003
        mock_instance.criar.return_value = Funcionario(
            matricula="F003",
            nome="Carlos Silva",
            idade=40,
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="55566677788",
            email="carlos@scb.com",
            senha="carlos123"
        )

        response = client.post("/funcionario", json=dados_funcionario_valido)

        assert response.status_code == 201
        data = response.json()
        assert data["matricula"] == "F003"
        assert data["nome"] == "Carlos Silva"
        assert data["funcao"] == "ADMINISTRATIVO"
        mock_instance.criar.assert_called_once()


def test_cadastrar_funcionario_idade_menor_18():
    """UC15 - R1: Testa erro quando idade < 18"""
    dados_invalidos = {
        "nome": "João Silva",
        "idade": 17,  # Menor de idade
        "funcao": "ADMINISTRATIVO",
        "cpf": "12345678901",
        "email": "joao@scb.com",
        "senha": "senha123",
        "confirmacaoSenha": "senha123"
    }

    response = client.post("/funcionario", json=dados_invalidos)

    assert response.status_code == 422


def test_cadastrar_funcionario_cpf_invalido():
    """UC15 - R2: Testa erro quando CPF não tem 11 dígitos"""
    dados_invalidos = {
        "nome": "João Silva",
        "idade": 30,
        "funcao": "ADMINISTRATIVO",
        "cpf": "123456789",  # 9 dígitos
        "email": "joao@scb.com",
        "senha": "senha123",
        "confirmacaoSenha": "senha123"
    }

    response = client.post("/funcionario", json=dados_invalidos)

    assert response.status_code == 422


def test_cadastrar_funcionario_senhas_diferentes():
    """UC15 - R4: Testa erro quando senhas não conferem"""
    dados_invalidos = {
        "nome": "João Silva",
        "idade": 30,
        "funcao": "ADMINISTRATIVO",
        "cpf": "12345678901",
        "email": "joao@scb.com",
        "senha": "senha123",
        "confirmacaoSenha": "senha456"  # Diferente
    }

    response = client.post("/funcionario", json=dados_invalidos)

    assert response.status_code == 422


def test_cadastrar_funcionario_campos_faltando():
    """UC15 - Testa erro quando faltam campos obrigatórios"""
    dados_incompletos = {
        "nome": "João Silva",
        "idade": 30
        # Faltam outros campos
    }

    response = client.post("/funcionario", json=dados_incompletos)

    assert response.status_code == 422


#   TESTES PUT /funcionario/{matricula}

def test_atualizar_funcionario_sucesso(funcionario_exemplo):
    """UC15 - Testa atualização de funcionário - sucesso"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance

        # Funcionário atualizado
        funcionario_atualizado = Funcionario(
            matricula="F001",
            nome="Admin Sistema Atualizado",  # Nome atualizado
            idade=36,  # Idade atualizada
            funcao=FuncaoFuncionario.ADMINISTRATIVO,
            cpf="12345678901",
            email="admin.novo@scb.com",  # Email atualizado
            senha="nova_senha"
        )

        mock_instance.atualizar.return_value = funcionario_atualizado

        dados_atualizacao = {
            "nome": "Admin Sistema Atualizado",
            "idade": 36,
            "funcao": "ADMINISTRATIVO",
            "cpf": "12345678901",
            "email": "admin.novo@scb.com",
            "senha": "nova_senha",
            "confirmacaoSenha": "nova_senha"
        }

        response = client.put("/funcionario/F001", json=dados_atualizacao)

        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Admin Sistema Atualizado"
        assert data["idade"] == 36
        assert data["email"] == "admin.novo@scb.com"
        mock_instance.atualizar.assert_called_once()


def test_atualizar_funcionario_nao_encontrado():
    """UC15 - Testa erro ao atualizar funcionário inexistente"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.atualizar.return_value = None

        dados_atualizacao = {
            "nome": "João Silva",
            "idade": 30,
            "funcao": "REPARADOR",
            "cpf": "11122233344",
            "email": "joao@scb.com",
            "senha": "senha123",
            "confirmacaoSenha": "senha123"
        }

        response = client.put("/funcionario/F999", json=dados_atualizacao)

        assert response.status_code == 404


#   TESTES DELETE /funcionario/{matricula}

def test_deletar_funcionario_sucesso():
    """UC15 - Testa remoção de funcionário - sucesso"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.deletar.return_value = True

        response = client.delete("/funcionario/F003")

        assert response.status_code == 200
        data = response.json()
        assert "removido com sucesso" in data["message"].lower() or "message" in data
        mock_instance.deletar.assert_called_once_with("F003")


def test_deletar_funcionario_nao_encontrado():
    """UC15 - Testa erro ao remover funcionário inexistente"""
    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.deletar.return_value = False

        response = client.delete("/funcionario/F999")

        assert response.status_code == 404


#   TESTES DE VALIDAÇÃO ADICIONAL

def test_cadastrar_funcionario_funcao_reparador(dados_funcionario_valido):
    """UC15 - R3: Testa cadastro com função REPARADOR"""
    dados_funcionario_valido["funcao"] = "REPARADOR"

    with patch('routers.funcionario.get_db'), \
         patch('routers.funcionario.FuncionarioRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance

        mock_instance.criar.return_value = Funcionario(
            matricula="F004",
            nome="Carlos Silva",
            idade=40,
            funcao=FuncaoFuncionario.REPARADOR,
            cpf="55566677788",
            email="carlos@scb.com",
            senha="carlos123"
        )

        response = client.post("/funcionario", json=dados_funcionario_valido)

        assert response.status_code == 201
        data = response.json()
        assert data["funcao"] == "REPARADOR"


def test_cadastrar_funcionario_email_invalido():
    """UC15 - Testa erro quando email é inválido"""
    dados_invalidos = {
        "nome": "João Silva",
        "idade": 30,
        "funcao": "ADMINISTRATIVO",
        "cpf": "12345678901",
        "email": "emailinvalido",  # Sem @
        "senha": "senha123",
        "confirmacaoSenha": "senha123"
    }

    response = client.post("/funcionario", json=dados_invalidos)

    assert response.status_code == 422
