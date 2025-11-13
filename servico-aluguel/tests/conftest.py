import os
import sys
import pytest
from unittest.mock import MagicMock
from datetime import date, datetime

CURRENT_DIR = os.path.dirname(__file__)
SERVICE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if SERVICE_ROOT not in sys.path:
    sys.path.insert(0, SERVICE_ROOT)

from models.ciclista_model import NovoCiclista, Ciclista, StatusCiclista, Nacionalidade, Passaporte
from models.funcionario_model import NovoFuncionario, Funcionario, FuncaoFuncionario
from models.cartao_model import NovoCartaoDeCredito, CartaoDeCredito



@pytest.fixture
def mock_db():
    """Mock do TinyDB"""
    return MagicMock()



@pytest.fixture
def ciclista_exemplo():
    """Ciclista padrão ATIVO para testes"""
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
        dataConfirmacao=datetime(2024, 1, 15, 10, 0, 0)
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
        urlFotoDocumento="http://exemplo.com/foto2.jpg",
        status=StatusCiclista.AGUARDANDO_CONFIRMACAO,
        senha="senha456",
        dataConfirmacao=None
    )


@pytest.fixture
def novo_ciclista_valido():
    """Dados válidos para criar novo ciclista BRASILEIRO"""
    return NovoCiclista(
        nome="Carlos Pereira",
        nascimento=date(1985, 3, 20),
        cpf="11122233344",
        email="carlos@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto3.jpg"
    )


@pytest.fixture
def novo_ciclista_estrangeiro():
    """Dados válidos para criar novo ciclista ESTRANGEIRO com passaporte"""
    return NovoCiclista(
        nome="John Doe",
        nascimento=date(1988, 7, 15),
        email="john@email.com",
        nacionalidade=Nacionalidade.ESTRANGEIRO,
        urlFotoDocumento="http://exemplo.com/foto4.jpg",
        passaporte=Passaporte(
            numero="AB123456",
            validade=date(2030, 12, 31),
            pais="USA"
        )
    )



@pytest.fixture
def funcionario_exemplo():
    """Funcionário ADMINISTRATIVO padrão para testes"""
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
def novo_funcionario_valido():
    """Dados válidos para criar novo funcionário"""
    return NovoFuncionario(
        nome="Carlos Silva",
        idade=40,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="55566677788",
        email="carlos@scb.com",
        senha="carlos123",
        confirmacaoSenha="carlos123"
    )



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
def novo_cartao_valido():
    """Dados válidos para criar novo cartão"""
    return NovoCartaoDeCredito(
        nomeTitular="Maria Santos",
        numero="9876543210987654",
        validade="06/26",
        cvv="456"
    )
