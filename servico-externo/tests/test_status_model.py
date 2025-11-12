"""
Testes unitários para o modelo de status.
"""

import pytest
from models.status_model import StatusResposta


def test_status_resposta_criacao():
    """Testa criação de StatusResposta"""
    status = StatusResposta(
        mensagem="Serviço operacional",
        status="OK"
    )
    
    assert status.mensagem == "Serviço operacional"
    assert status.status == "OK"


def test_status_resposta_model_dump():
    """Testa serialização do modelo"""
    status = StatusResposta(
        mensagem="Teste",
        status="Operacional"
    )
    
    data = status.model_dump()
    assert data["mensagem"] == "Teste"
    assert data["status"] == "Operacional"

