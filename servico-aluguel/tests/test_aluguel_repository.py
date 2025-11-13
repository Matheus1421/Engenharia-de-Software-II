"""Testes para repositories/aluguel_repository.py"""
from unittest.mock import MagicMock
from repositories.aluguel_repository import AluguelRepository

def test_criar_cobranca_gera_id_automatico():
    """Testa que criar_cobranca gera ID sequencial"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []

    repo = AluguelRepository(mock_db)
    cobranca = repo.criar_cobranca(10.0, 1, "ALUGUEL_INICIAL")

    assert cobranca.id == 1
    assert cobranca.valor == 10.0
    assert cobranca.status == "PAGA"

def test_criar_cobranca_id_sequencial():
    """Testa IDs sequenciais (1, 2, 3...)"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = [{'id': 1}, {'id': 2}]

    repo = AluguelRepository(mock_db)
    cobranca = repo.criar_cobranca(5.0, 2, "TAXA_EXTRA")

    assert cobranca.id == 3
