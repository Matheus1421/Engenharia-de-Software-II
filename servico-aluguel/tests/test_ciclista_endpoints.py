"""
Testes unitários dos endpoints de ciclista.
Cobre UC01 (Cadastrar), UC02 (Ativar Email), UC06 (Alterar Dados).
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import date

from main import app
from models.ciclista_model import Ciclista, StatusCiclista, Nacionalidade
from models.cartao_model import CartaoDeCredito

client = TestClient(app)


#   FIXTURES

@pytest.fixture
def ciclista_exemplo():
    """Ciclista ATIVO para testes"""
    return Ciclista(
        id=1,
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg",
        status=StatusCiclista.ATIVO,
        senha="senha123",
        dataConfirmacao="2024-01-15T10:00:00Z"
    )


@pytest.fixture
def ciclista_aguardando():
    """Ciclista AGUARDANDO_CONFIRMACAO para testes"""
    return Ciclista(
        id=2,
        nome="Maria Santos",
        nascimento=date(1995, 5, 10),
        cpf="98765432100",
        email="maria@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg",
        status=StatusCiclista.AGUARDANDO_CONFIRMACAO,
        senha="senha456",
        dataConfirmacao=None
    )


@pytest.fixture
def dados_cadastro_valido():
    """Dados válidos para cadastro de ciclista (UC01)"""
    return {
        "ciclista": {
            "nome": "Carlos Pereira",
            "nascimento": "1985-03-20",
            "cpf": "11122233344",
            "email": "carlos@email.com",
            "nacionalidade": "BRASILEIRO",
            "urlFotoDocumento": "http://exemplo.com/foto.jpg"
        },
        "senha": "senha123",
        "confirmacaoSenha": "senha123"
    }


@pytest.fixture
def dados_cartao_valido():
    """Dados válidos de cartão de crédito"""
    return {
        "nomeTitular": "Carlos Pereira",
        "numero": "1234567890123456",
        "validade": "12/25",
        "cvv": "123"
    }


#   TESTES POST /ciclista (UC01)

def test_cadastrar_ciclista_cartao_invalido(dados_cadastro_valido, dados_cartao_valido):
    """UC01 - Passo 7: Testa erro quando cartão é inválido"""
    with patch('routers.ciclista.get_db'), \
         patch('routers.ciclista.CiclistaRepository') as mock_repo, \
         patch('routers.ciclista.pagamento_service') as mock_pag:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_email.return_value = None

        # Cartão inválido
        mock_pag.validar_cartao.return_value = {"valido": False}

        response = client.post(
            "/ciclista",
            json=dados_cadastro_valido,
            params=dados_cartao_valido
        )

        assert response.status_code == 422


def test_cadastrar_ciclista_senhas_diferentes():
    """UC01 - R2: Testa erro quando senhas não conferem"""
    dados_invalidos = {
        "ciclista": {
            "nome": "Carlos Pereira",
            "nascimento": "1985-03-20",
            "cpf": "11122233344",
            "email": "carlos@email.com",
            "nacionalidade": "BRASILEIRO",
            "urlFotoDocumento": "http://exemplo.com/foto.jpg"
        },
        "senha": "senha123",
        "confirmacaoSenha": "senha456"  # Diferente
    }

    response = client.post("/ciclista", json=dados_invalidos)

    # Falha na validação Pydantic
    assert response.status_code == 422


def test_cadastrar_ciclista_cpf_invalido():
    """UC01 - R1: Testa erro quando CPF não tem 11 dígitos"""
    dados_invalidos = {
        "ciclista": {
            "nome": "Carlos Pereira",
            "nascimento": "1985-03-20",
            "cpf": "123456789",  # Menos de 11 dígitos
            "email": "carlos@email.com",
            "nacionalidade": "BRASILEIRO",
            "urlFotoDocumento": "http://exemplo.com/foto.jpg"
        },
        "senha": "senha123",
        "confirmacaoSenha": "senha123"
    }

    response = client.post("/ciclista", json=dados_invalidos)

    assert response.status_code == 422


#   TESTES POST /ciclista/{id}/ativar (UC02)

#   TESTES GET /ciclista/{id}

def test_buscar_ciclista_sucesso(ciclista_exemplo):
    """Testa busca de ciclista por ID - sucesso"""
    with patch('routers.ciclista.get_db'), \
         patch('routers.ciclista.CiclistaRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_id.return_value = ciclista_exemplo

        response = client.get("/ciclista/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "joao@email.com"
        mock_instance.buscar_por_id.assert_called_once_with(1)


def test_buscar_ciclista_nao_encontrado():
    """Testa erro ao buscar ciclista inexistente"""
    with patch('routers.ciclista.get_db'), \
         patch('routers.ciclista.CiclistaRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_id.return_value = None

        response = client.get("/ciclista/999")

        assert response.status_code == 404


#   TESTES PUT /ciclista/{id} (UC06)

def test_atualizar_ciclista_sucesso(ciclista_exemplo):
    """UC06 - Testa atualização de dados do ciclista"""
    with patch('routers.ciclista.get_db'), \
         patch('routers.ciclista.CiclistaRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance

        # Ciclista atualizado
        ciclista_atualizado = Ciclista(
            id=1,
            nome="João Silva",
            nascimento=date(1990, 1, 1),
            cpf="12345678901",
            email="joao@email.com",
            nacionalidade=Nacionalidade.BRASILEIRO,
            urlFotoDocumento="http://exemplo.com/foto_nova.jpg",  # URL atualizada
            status=StatusCiclista.ATIVO,
            senha="senha123",
            dataConfirmacao="2024-01-15T10:00:00Z"
        )

        mock_instance.atualizar.return_value = ciclista_atualizado

        dados_atualizacao = {
            "nome": "João Silva",
            "nascimento": "1990-01-01",
            "cpf": "12345678901",
            "email": "joao@email.com",
            "nacionalidade": "BRASILEIRO",
            "urlFotoDocumento": "http://exemplo.com/foto_nova.jpg"
        }

        response = client.put("/ciclista/1", json=dados_atualizacao)

        assert response.status_code == 200
        data = response.json()
        assert data["urlFotoDocumento"] == "http://exemplo.com/foto_nova.jpg"
        mock_instance.atualizar.assert_called_once()


#   TESTES GET /ciclista/{id}/permiteAluguel

#   TESTES GET /ciclista/{id}/bicicletaAlugada

#   TESTES GET /ciclista/existeEmail/{email}

def test_existe_email_encontrado(ciclista_exemplo):
    """Testa verificação quando email existe"""
    with patch('routers.ciclista.get_db'), \
         patch('routers.ciclista.CiclistaRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_email.return_value = ciclista_exemplo

        response = client.get("/ciclista/existeEmail/joao@email.com")

        assert response.status_code == 200
        assert response.json() == True


def test_existe_email_nao_encontrado():
    """Testa verificação quando email não existe"""
    with patch('routers.ciclista.get_db'), \
         patch('routers.ciclista.CiclistaRepository') as mock_repo:

        mock_instance = Mock()
        mock_repo.return_value = mock_instance
        mock_instance.buscar_por_email.return_value = None

        response = client.get("/ciclista/existeEmail/naoexiste@email.com")

        assert response.status_code == 200
        assert response.json() == False
