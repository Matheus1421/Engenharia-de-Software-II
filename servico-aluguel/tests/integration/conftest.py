"""
Fixtures compartilhadas para testes de integração.

Conforme Cap. 8 - Engenharia de Software Moderna:
- Cada teste deve ser independente (Independent)
- Resultados devem ser determinísticos (Repeatable)
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from main import app
from database.database import get_db, reset_db
from database.init_data import init_db


@pytest.fixture
def client():
    """TestClient do FastAPI para requisições HTTP"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """
    Fixture que reseta o banco antes de cada teste.
    Garante independência entre testes (princípio FIRST).
    """
    reset_db()
    db = get_db()
    init_db(db)
    yield
    # Cleanup após o teste (opcional)


@pytest.fixture
def db():
    """Retorna instância do banco de dados"""
    return get_db()


@pytest.fixture
def ciclista_ativo(db):
    """
    Ciclista com status ATIVO no banco.
    Retorna o ID do ciclista.
    """
    # Ciclista 1 já existe no init_data com status ATIVO
    return 1


@pytest.fixture
def ciclista_inativo(db):
    """
    Ciclista com status AGUARDANDO_CONFIRMACAO.
    Retorna o ID do ciclista.
    """
    # Ciclista 2 já existe no init_data com status AGUARDANDO_CONFIRMACAO
    return 2


@pytest.fixture
def ciclista_com_aluguel_ativo(db):
    """
    Ciclista que já possui um aluguel em andamento.
    Retorna o ID do ciclista.
    """
    # Ciclista 3 já tem aluguel ativo no init_data
    return 3


@pytest.fixture
def dados_aluguel_valido(ciclista_ativo):
    """Payload válido para POST /aluguel"""
    return {
        "ciclista": ciclista_ativo,
        "trancaInicio": 1  # Tranca 1 tem bicicleta 1 (DISPONIVEL)
    }


@pytest.fixture
def dados_devolucao_valido():
    """Payload válido para POST /devolucao"""
    return {
        "idTranca": 2,  # Tranca disponível para devolução
        "idBicicleta": 3  # Bicicleta do aluguel do ciclista 3
    }


@pytest.fixture
def dados_ciclista_valido():
    """Payload válido para POST /ciclista"""
    return {
        "nome": "Novo Ciclista",
        "nascimento": "1990-05-15",
        "cpf": "12345678901",
        "nacionalidade": "BRASILEIRO",
        "email": "novo@example.com",
        "urlFotoDocumento": "https://exemplo.com/foto.jpg",
        "senha": "SenhaSegura123",
        "meioDePagamento": {
            "nomeTitular": "Novo Ciclista",
            "numero": "4111111111111111",
            "validade": "12/28",
            "cvv": "123"
        }
    }


# ============================================================
# CONSTANTES PARA MOCKS - URLs dos serviços externos
# ============================================================

EQUIPAMENTO_URL = "http://localhost:8000"
EXTERNO_URL = "http://localhost:8002"


@pytest.fixture
def mock_bicicleta_disponivel():
    """Resposta mock: bicicleta disponível na tranca"""
    return {
        "id": 1,
        "marca": "Caloi",
        "modelo": "Caloi",
        "ano": "2020",
        "numero": 12345,
        "status": "DISPONIVEL"
    }


@pytest.fixture
def mock_cobranca_aprovada():
    """Resposta mock: cobrança aprovada"""
    return {
        "id": 100,
        "status": "PAGA",
        "valor": 10.00,
        "ciclista": 1,
        "horaSolicitacao": datetime.now().isoformat(),
        "horaFinalizacao": datetime.now().isoformat()
    }


@pytest.fixture
def mock_cobranca_recusada():
    """Resposta mock: cobrança recusada"""
    return {
        "id": 100,
        "status": "RECUSADA",
        "valor": 10.00,
        "ciclista": 1
    }


@pytest.fixture
def mock_tranca_destrancada():
    """Resposta mock: tranca destrancada com sucesso"""
    return {
        "id": 1,
        "status": "LIVRE",
        "bicicleta": None
    }


@pytest.fixture
def mock_tranca_trancada():
    """Resposta mock: tranca trancada com sucesso"""
    return {
        "id": 2,
        "status": "OCUPADA",
        "bicicleta": 3
    }


@pytest.fixture
def mock_email_enviado():
    """Resposta mock: email enviado com sucesso"""
    return {
        "id": 1,
        "destinatario": "user@example.com",
        "assunto": "Aluguel realizado",
        "enviado": True
    }


@pytest.fixture
def mock_cartao_valido():
    """Resposta mock: cartão válido"""
    return {
        "valido": True,
        "mensagem": "Cartão válido"
    }


@pytest.fixture
def mock_cartao_invalido():
    """Resposta mock: cartão inválido"""
    return {
        "valido": False,
        "mensagem": "Cartão recusado"
    }
