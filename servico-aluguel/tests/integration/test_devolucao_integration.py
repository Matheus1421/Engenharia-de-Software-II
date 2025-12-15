"""
Testes de Integração - UC04: Devolver Bicicleta

Conforme Cap. 8 - Engenharia de Software Moderna:
- Testes de integração exercitam funcionalidades de maior granularidade
- Usamos mocks HTTP para simular microsserviços externos
- Seguimos princípios FIRST (Fast, Independent, Repeatable, Self-validating, Timely)

Integrações testadas:
- equipamento_service.trancar()
- email_service.enviar_recibo_devolucao()
"""
import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from main import app
from database.database import get_db
from tests.integration.conftest import EQUIPAMENTO_URL, EXTERNO_URL


client = TestClient(app)


# ============================================================
# TESTES DE FLUXO COMPLETO (Happy Path)
# ============================================================

@respx.mock
def test_devolucao_sucesso_sem_taxa_extra(
    setup_db,
    mock_tranca_trancada,
    mock_email_enviado
):
    """
    UC04 - Devolução em menos de 2 horas - apenas R$ 10,00.

    Ciclista 3 tem aluguel ativo com bicicleta 3.
    """
    # Mock: POST /tranca/{id}/trancar - sucesso
    respx.post(f"{EQUIPAMENTO_URL}/tranca/2/trancar").mock(
        return_value=Response(200, json=mock_tranca_trancada)
    )

    # Mock: POST /email/enviar - sucesso
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    dados = {
        "idTranca": 2,
        "idBicicleta": 3  # Bicicleta do aluguel do ciclista 3
    }

    response = client.post("/devolucao", json=dados)

    assert response.status_code == 200
    data = response.json()

    assert data["aluguel"]["status"] == "FINALIZADO"
    assert data["valorTotal"] >= 10.00  # Mínimo R$ 10,00
    assert data["tempoTotal"] >= 0


@respx.mock
def test_devolucao_sucesso_com_taxa_extra(setup_db, db, mock_tranca_trancada, mock_email_enviado):
    """
    UC04 - Devolução após 2 horas - R$ 10,00 + taxa extra.

    Modifica o aluguel no banco para simular início há mais de 2 horas.
    """
    from tinydb import Query
    Aluguel = Query()

    # Modifica a hora de início do aluguel do ciclista 4 para 3 horas atrás
    tres_horas_atras = (datetime.now() - timedelta(hours=3)).isoformat()
    db.table('alugueis').update(
        {"horaInicio": tres_horas_atras},
        (Aluguel.ciclista == 4) & (Aluguel.status == "EM_ANDAMENTO")
    )

    # Mock: POST /tranca/{id}/trancar - sucesso
    respx.post(f"{EQUIPAMENTO_URL}/tranca/2/trancar").mock(
        return_value=Response(200, json=mock_tranca_trancada)
    )

    # Mock: POST /email/enviar - sucesso
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    dados = {
        "idTranca": 2,
        "idBicicleta": 5  # Bicicleta do aluguel do ciclista 4
    }

    response = client.post("/devolucao", json=dados)

    assert response.status_code == 200
    data = response.json()

    assert data["aluguel"]["status"] == "FINALIZADO"
    assert data["taxaExtra"] > 0  # Deve ter taxa extra
    assert data["valorTotal"] > 10.00  # Mais que R$ 10,00


# ============================================================
# TESTES DE FALHA - INTEGRAÇÃO COM EQUIPAMENTO
# ============================================================

@respx.mock
def test_devolucao_falha_trancar(setup_db):
    """
    UC04 - Falha quando não consegue trancar a bicicleta.

    Mock retorna erro ao tentar trancar.
    """
    # Mock: POST /tranca/{id}/trancar - FALHA
    respx.post(f"{EQUIPAMENTO_URL}/tranca/2/trancar").mock(
        return_value=Response(500, json={"detail": "Erro ao trancar"})
    )

    dados = {
        "idTranca": 2,
        "idBicicleta": 3
    }

    response = client.post("/devolucao", json=dados)

    assert response.status_code == 500
    assert "trancar" in response.json()["detail"].lower()


@respx.mock
def test_devolucao_falha_equipamento_timeout(setup_db):
    """
    UC04 - Falha quando o serviço de equipamento não responde.

    Simula timeout do serviço externo.
    """
    import httpx

    # Mock: POST /tranca/{id}/trancar - timeout
    respx.post(f"{EQUIPAMENTO_URL}/tranca/2/trancar").mock(
        side_effect=httpx.TimeoutException("Timeout")
    )

    dados = {
        "idTranca": 2,
        "idBicicleta": 3
    }

    response = client.post("/devolucao", json=dados)

    assert response.status_code == 500


# ============================================================
# TESTES DE FALHA NÃO-CRÍTICA - EMAIL
# ============================================================

@respx.mock
def test_devolucao_sucesso_mesmo_com_falha_email(setup_db, mock_tranca_trancada):
    """
    UC04 - Devolução deve ser bem sucedida mesmo se o email falhar.

    O envio de email não é crítico para a operação.
    """
    # Mock: POST /tranca/{id}/trancar - sucesso
    respx.post(f"{EQUIPAMENTO_URL}/tranca/2/trancar").mock(
        return_value=Response(200, json=mock_tranca_trancada)
    )

    # Mock: POST /email/enviar - FALHA
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(500, json={"detail": "Erro ao enviar email"})
    )

    dados = {
        "idTranca": 2,
        "idBicicleta": 3
    }

    response = client.post("/devolucao", json=dados)

    # Devolução deve funcionar mesmo com falha no email
    assert response.status_code == 200
    data = response.json()
    assert data["aluguel"]["status"] == "FINALIZADO"


# ============================================================
# TESTES DE VALIDAÇÃO DE NEGÓCIO
# ============================================================

@respx.mock
def test_devolucao_falha_sem_aluguel_ativo(setup_db):
    """
    UC04 - Falha ao tentar devolver bicicleta sem aluguel ativo.

    Validação de regra de negócio - sem chamadas externas.
    """
    dados = {
        "idTranca": 2,
        "idBicicleta": 999  # Bicicleta inexistente ou sem aluguel
    }

    response = client.post("/devolucao", json=dados)

    assert response.status_code == 422
    assert "aluguel" in response.json()["detail"].lower()


@respx.mock
def test_devolucao_falha_bicicleta_disponivel(setup_db):
    """
    UC04 - Falha ao tentar devolver bicicleta que não está alugada.

    Bicicleta 1 está DISPONIVEL (não alugada).
    """
    dados = {
        "idTranca": 2,
        "idBicicleta": 1  # Bicicleta disponível, não alugada
    }

    response = client.post("/devolucao", json=dados)

    assert response.status_code == 422


# ============================================================
# TESTES DE VERIFICAÇÃO DO BANCO DE DADOS
# ============================================================

@respx.mock
def test_devolucao_atualiza_banco(setup_db, db, mock_tranca_trancada, mock_email_enviado):
    """
    UC04 - Verifica se a devolução atualiza corretamente o banco.

    Princípio: Self-validating - valida estado do banco após operação.
    """
    from tinydb import Query
    Aluguel = Query()

    # Mock: POST /tranca/{id}/trancar - sucesso
    respx.post(f"{EQUIPAMENTO_URL}/tranca/2/trancar").mock(
        return_value=Response(200, json=mock_tranca_trancada)
    )

    # Mock: POST /email/enviar - sucesso
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    dados = {
        "idTranca": 2,
        "idBicicleta": 3
    }

    # Executa devolução
    response = client.post("/devolucao", json=dados)
    assert response.status_code == 200

    # Verifica se o aluguel foi atualizado no banco
    aluguel = db.table('alugueis').get(
        (Aluguel.idBicicleta == 3) & (Aluguel.status == "FINALIZADO")
    )

    assert aluguel is not None
    assert aluguel["trancaFim"] == 2
    assert aluguel["horaFim"] is not None
