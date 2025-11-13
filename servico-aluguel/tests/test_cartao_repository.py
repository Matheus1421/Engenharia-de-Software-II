"""
Testes unitários do CartaoRepository.
Testa operações de CRUD de cartões de crédito (UC07).
"""
import pytest
from unittest.mock import MagicMock, Mock
from repositories.cartao_repository import CartaoRepository
from models.cartao_model import NovoCartaoDeCredito, CartaoDeCredito


#   TESTES DE CRIAR (UC07)

def test_criar_cartao_gera_id_automatico():
    """UC07 - Testa que criar() gera ID automático"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []  # Banco vazio
    mock_table.insert = Mock()

    repo = CartaoRepository(mock_db)

    cartao_dados = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",
        cvv="123"
    )

    resultado = repo.criar(id_ciclista=1, cartao=cartao_dados)

    assert resultado.id == 1
    assert resultado.idCiclista == 1
    assert resultado.nomeTitular == "João Silva"
    mock_table.insert.assert_called_once()


def test_criar_cartao_id_sequencial():
    """UC07 - Testa que criar() gera IDs sequenciais"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Simula 1 cartão já existente
    mock_table.all.return_value = [{'id': 1}]
    mock_table.insert = Mock()

    repo = CartaoRepository(mock_db)

    cartao_dados = NovoCartaoDeCredito(
        nomeTitular="Maria Santos",
        numero="9876543210987654",
        validade="06/26",
        cvv="456"
    )

    resultado = repo.criar(id_ciclista=2, cartao=cartao_dados)

    assert resultado.id == 2  # Sequencial


#   TESTES DE BUSCAR_POR_ID

def test_buscar_por_id_encontra():
    """UC07 - Testa buscar_por_id quando cartão existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.get.return_value = {
        'id': 1,
        'nomeTitular': 'João Silva',
        'numero': '1234567890123456',
        'validade': '12/25',
        'cvv': '123',
        'idCiclista': 1
    }

    repo = CartaoRepository(mock_db)
    resultado = repo.buscar_por_id(1)

    assert resultado is not None
    assert resultado.id == 1
    assert resultado.nomeTitular == "João Silva"


def test_buscar_por_id_nao_encontra():
    """UC07 - Testa buscar_por_id quando cartão não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CartaoRepository(mock_db)
    resultado = repo.buscar_por_id(999)

    assert resultado is None


#   TESTES DE BUSCAR_POR_CICLISTA

def test_buscar_por_ciclista_encontra():
    """UC07 - Testa buscar_por_ciclista quando ciclista tem cartão"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.get.return_value = {
        'id': 1,
        'nomeTitular': 'João Silva',
        'numero': '1234567890123456',
        'validade': '12/25',
        'cvv': '123',
        'idCiclista': 1
    }

    repo = CartaoRepository(mock_db)
    resultado = repo.buscar_por_ciclista(id_ciclista=1)

    assert resultado is not None
    assert resultado.idCiclista == 1


def test_buscar_por_ciclista_nao_encontra():
    """UC07 - Testa buscar_por_ciclista quando ciclista não tem cartão"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CartaoRepository(mock_db)
    resultado = repo.buscar_por_ciclista(id_ciclista=999)

    assert resultado is None


#   TESTES DE ATUALIZAR (UC07)

def test_atualizar_cartao_sucesso():
    """UC07 - Testa que atualizar() modifica os dados"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Cartão antes
    cartao_antes = {
        'id': 1,
        'nomeTitular': 'João Silva',
        'numero': '1234567890123456',
        'validade': '12/25',
        'cvv': '123',
        'idCiclista': 1
    }

    # Cartão depois (buscar_por_ciclista remove cvv e numeroCompleto)
    cartao_depois = {
        'id': 1,
        'nomeTitular': 'João Silva',
        'numero': '**** **** **** 3456',
        'validade': '06/26',
        'idCiclista': 1
    }

    # Precisamos mockar duas chamadas ao get():
    # 1ª: buscar_por_id(1) -> retorna cartao_antes (para pegar idCiclista)
    # 2ª: buscar_por_ciclista(1) -> retorna cartao_depois
    mock_table.get.side_effect = [cartao_antes, cartao_depois]
    mock_table.update = Mock()

    repo = CartaoRepository(mock_db)

    dados_novos = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="06/26",  # Nova validade
        cvv="456"  # Novo CVV
    )

    resultado = repo.atualizar(id=1, cartao=dados_novos)

    assert resultado is not None
    assert resultado.validade == "06/26"
    # cvv não é retornado por buscar_por_ciclista
    mock_table.update.assert_called_once()


def test_atualizar_cartao_nao_encontrado():
    """UC07 - Testa que atualizar() retorna None quando cartão não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CartaoRepository(mock_db)

    dados_novos = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",
        cvv="123"
    )

    resultado = repo.atualizar(id=999, cartao=dados_novos)

    assert resultado is None


#   TESTES DE DELETAR (UC07)

def test_deletar_cartao_sucesso():
    """UC07 - Testa que deletar() remove o cartão"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Cartão existe
    mock_table.get.return_value = {
        'id': 1,
        'nomeTitular': 'João Silva',
        'numero': '1234567890123456',
        'validade': '12/25',
        'cvv': '123',
        'idCiclista': 1
    }
    mock_table.remove = Mock(return_value=[1])  # Lista com 1 documento removido

    repo = CartaoRepository(mock_db)
    resultado = repo.deletar(id=1)

    assert resultado is True
    mock_table.remove.assert_called_once()


def test_deletar_cartao_nao_encontrado():
    """UC07 - Testa que deletar() retorna False quando cartão não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CartaoRepository(mock_db)
    resultado = repo.deletar(id=999)

    assert resultado is False


#   TESTES DE LISTAR

def test_listar_retorna_todos():
    """UC07 - Testa que listar() retorna todos os cartões"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.all.return_value = [
        {
            'id': 1,
            'nomeTitular': 'João Silva',
            'numero': '1234567890123456',
            'validade': '12/25',
            'cvv': '123',
            'idCiclista': 1
        },
        {
            'id': 2,
            'nomeTitular': 'Maria Santos',
            'numero': '9876543210987654',
            'validade': '06/26',
            'cvv': '456',
            'idCiclista': 2
        }
    ]

    repo = CartaoRepository(mock_db)
    resultado = repo.listar()

    assert len(resultado) == 2
    assert resultado[0].id == 1
    assert resultado[1].id == 2


def test_listar_retorna_lista_vazia():
    """UC07 - Testa que listar() retorna [] quando não há cartões"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []

    repo = CartaoRepository(mock_db)
    resultado = repo.listar()

    assert resultado == []
