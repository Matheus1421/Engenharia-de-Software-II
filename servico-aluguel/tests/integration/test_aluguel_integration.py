"""
Testes de Integração - UC03: Alugar Bicicleta

Conforme Cap. 8 - Engenharia de Software Moderna:
- Testes de integração exercitam funcionalidades de maior granularidade
- Usamos mocks HTTP para simular microsserviços externos
- Seguimos princípios FIRST (Fast, Independent, Repeatable, Self-validating, Timely)

Integrações testadas:
- equipamento_service.obter_bicicleta_tranca()
- pagamento_service.cobrar()
- equipamento_service.destrancar()
- email_service.enviar_recibo_aluguel()
"""
import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient

from main import app
from tests.integration.conftest import EQUIPAMENTO_URL, EXTERNO_URL


client = TestClient(app)


# ============================================================
# TESTES DE FLUXO COMPLETO (Happy Path)
# ============================================================

@respx.mock
def test_aluguel_sucesso_fluxo_completo(
    setup_db,
    dados_aluguel_valido,
    mock_bicicleta_disponivel,
    mock_cobranca_aprovada,
    mock_tranca_destrancada,
    mock_email_enviado
):
    """
    UC03 - Testa o fluxo completo de aluguel com sucesso.

    Passos:
    1. Ciclista ativo no banco (fixture)
    2. Bicicleta disponível na tranca (mock equipamento)
    3. Cobrança aprovada (mock pagamento)
    4. Tranca destrancada (mock equipamento)
    5. Email enviado (mock email)
    6. Aluguel registrado no banco
    """
    # Mock: GET /tranca/{id}/bicicleta - retorna bicicleta disponível
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(200, json=mock_bicicleta_disponivel)
    )

    # Mock: POST /cobranca - cobrança aprovada
    respx.post(f"{EXTERNO_URL}/cobranca").mock(
        return_value=Response(200, json=mock_cobranca_aprovada)
    )

    # Mock: POST /tranca/{id}/destrancar - tranca destrancada
    respx.post(f"{EQUIPAMENTO_URL}/tranca/1/destrancar").mock(
        return_value=Response(200, json=mock_tranca_destrancada)
    )

    # Mock: POST /email/enviar - email enviado
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    # Executa requisição
    response = client.post("/aluguel", json=dados_aluguel_valido)

    # Validações
    assert response.status_code == 200
    data = response.json()

    assert data["ciclista"] == dados_aluguel_valido["ciclista"]
    assert data["trancaInicio"] == dados_aluguel_valido["trancaInicio"]
    assert data["idBicicleta"] == mock_bicicleta_disponivel["id"]
    assert data["status"] == "EM_ANDAMENTO"
    assert data["cobranca"] is not None
    assert data["horaInicio"] is not None


# ============================================================
# TESTES DE FALHA - INTEGRAÇÃO COM EQUIPAMENTO
# ============================================================

@respx.mock
def test_aluguel_falha_tranca_sem_bicicleta(setup_db, dados_aluguel_valido):
    """
    UC03 - Falha quando a tranca não tem bicicleta.

    Mock retorna 404 simulando tranca vazia.
    """
    # Mock: GET /tranca/{id}/bicicleta - tranca vazia (404)
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(404, json={"detail": "Tranca sem bicicleta"})
    )

    response = client.post("/aluguel", json=dados_aluguel_valido)

    assert response.status_code == 422
    assert "bicicleta" in response.json()["detail"].lower()


@respx.mock
def test_aluguel_falha_equipamento_timeout(setup_db, dados_aluguel_valido):
    """
    UC03 - Falha quando o serviço de equipamento não responde (timeout).

    Simula timeout do serviço externo.
    """
    import httpx

    # Mock: GET /tranca/{id}/bicicleta - timeout
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        side_effect=httpx.TimeoutException("Timeout")
    )

    response = client.post("/aluguel", json=dados_aluguel_valido)

    assert response.status_code == 422


@respx.mock
def test_aluguel_falha_destrancar(
    setup_db,
    dados_aluguel_valido,
    mock_bicicleta_disponivel,
    mock_cobranca_aprovada
):
    """
    UC03 - Falha quando não consegue destrancar a tranca.

    A cobrança foi aprovada mas a tranca não abre.
    """
    # Mock: GET /tranca/{id}/bicicleta - sucesso
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(200, json=mock_bicicleta_disponivel)
    )

    # Mock: POST /cobranca - sucesso
    respx.post(f"{EXTERNO_URL}/cobranca").mock(
        return_value=Response(200, json=mock_cobranca_aprovada)
    )

    # Mock: POST /tranca/{id}/destrancar - FALHA
    respx.post(f"{EQUIPAMENTO_URL}/tranca/1/destrancar").mock(
        return_value=Response(500, json={"detail": "Erro ao destrancar"})
    )

    response = client.post("/aluguel", json=dados_aluguel_valido)

    assert response.status_code == 500
    assert "destrancar" in response.json()["detail"].lower()


# ============================================================
# TESTES DE FALHA - INTEGRAÇÃO COM PAGAMENTO
# ============================================================

@respx.mock
def test_aluguel_falha_pagamento_recusado(
    setup_db,
    dados_aluguel_valido,
    mock_bicicleta_disponivel,
    mock_cobranca_recusada
):
    """
    UC03 - Falha quando o pagamento é recusado.

    Mock retorna cobrança com status diferente de PAGA.
    """
    # Mock: GET /tranca/{id}/bicicleta - sucesso
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(200, json=mock_bicicleta_disponivel)
    )

    # Mock: POST /cobranca - RECUSADO
    respx.post(f"{EXTERNO_URL}/cobranca").mock(
        return_value=Response(200, json=mock_cobranca_recusada)
    )

    response = client.post("/aluguel", json=dados_aluguel_valido)

    assert response.status_code == 422
    assert "pagamento" in response.json()["detail"].lower() or "autorizado" in response.json()["detail"].lower()


@respx.mock
def test_aluguel_falha_pagamento_timeout(setup_db, dados_aluguel_valido, mock_bicicleta_disponivel):
    """
    UC03 - Falha quando o serviço de pagamento não responde.

    Simula timeout do serviço de pagamento.
    """
    import httpx

    # Mock: GET /tranca/{id}/bicicleta - sucesso
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(200, json=mock_bicicleta_disponivel)
    )

    # Mock: POST /cobranca - timeout
    respx.post(f"{EXTERNO_URL}/cobranca").mock(
        side_effect=httpx.TimeoutException("Timeout")
    )

    response = client.post("/aluguel", json=dados_aluguel_valido)

    assert response.status_code == 422


# ============================================================
# TESTES DE FALHA NÃO-CRÍTICA - EMAIL
# ============================================================

@respx.mock
def test_aluguel_sucesso_mesmo_com_falha_email(
    setup_db,
    dados_aluguel_valido,
    mock_bicicleta_disponivel,
    mock_cobranca_aprovada,
    mock_tranca_destrancada
):
    """
    UC03 - Aluguel deve ser bem sucedido mesmo se o email falhar.

    O envio de email não é crítico para a operação.
    """
    # Mock: GET /tranca/{id}/bicicleta - sucesso
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(200, json=mock_bicicleta_disponivel)
    )

    # Mock: POST /cobranca - sucesso
    respx.post(f"{EXTERNO_URL}/cobranca").mock(
        return_value=Response(200, json=mock_cobranca_aprovada)
    )

    # Mock: POST /tranca/{id}/destrancar - sucesso
    respx.post(f"{EQUIPAMENTO_URL}/tranca/1/destrancar").mock(
        return_value=Response(200, json=mock_tranca_destrancada)
    )

    # Mock: POST /email/enviar - FALHA (500)
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(500, json={"detail": "Erro ao enviar email"})
    )

    response = client.post("/aluguel", json=dados_aluguel_valido)

    # Aluguel deve funcionar mesmo com falha no email
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "EM_ANDAMENTO"


# ============================================================
# TESTES DE VALIDAÇÃO DE NEGÓCIO
# ============================================================

@respx.mock
def test_aluguel_falha_ciclista_inativo(setup_db, ciclista_inativo):
    """
    UC03 - Ciclista com status diferente de ATIVO não pode alugar.

    Validação de regra de negócio - sem chamadas externas.
    """
    dados = {
        "ciclista": ciclista_inativo,  # Ciclista 2 - AGUARDANDO_CONFIRMACAO
        "trancaInicio": 1
    }

    response = client.post("/aluguel", json=dados)

    assert response.status_code == 422
    assert "ciclista" in response.json()["detail"].lower()


@respx.mock
def test_aluguel_falha_ciclista_ja_tem_aluguel(setup_db, ciclista_com_aluguel_ativo):
    """
    UC03 - Ciclista que já possui aluguel ativo não pode alugar novamente.

    Validação de regra de negócio - sem chamadas externas.
    """
    dados = {
        "ciclista": ciclista_com_aluguel_ativo,  # Ciclista 3 - já tem aluguel
        "trancaInicio": 1
    }

    response = client.post("/aluguel", json=dados)

    assert response.status_code == 422
    assert "aluguel" in response.json()["detail"].lower()


# ============================================================
# TESTES DE VERIFICAÇÃO DO BANCO DE DADOS
# ============================================================

@respx.mock
def test_aluguel_registra_no_banco(
    setup_db,
    db,
    dados_aluguel_valido,
    mock_bicicleta_disponivel,
    mock_cobranca_aprovada,
    mock_tranca_destrancada,
    mock_email_enviado
):
    """
    UC03 - Verifica se o aluguel é corretamente persistido no banco.

    Princípio: Self-validating - valida estado do banco após operação.
    """
    # Configura mocks
    respx.get(f"{EQUIPAMENTO_URL}/tranca/1/bicicleta").mock(
        return_value=Response(200, json=mock_bicicleta_disponivel)
    )
    respx.post(f"{EXTERNO_URL}/cobranca").mock(
        return_value=Response(200, json=mock_cobranca_aprovada)
    )
    respx.post(f"{EQUIPAMENTO_URL}/tranca/1/destrancar").mock(
        return_value=Response(200, json=mock_tranca_destrancada)
    )
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    # Conta aluguéis antes
    alugueis_antes = len(db.table('alugueis').all())

    # Executa aluguel
    response = client.post("/aluguel", json=dados_aluguel_valido)
    assert response.status_code == 200

    # Verifica se foi registrado no banco
    alugueis_depois = len(db.table('alugueis').all())
    assert alugueis_depois == alugueis_antes + 1

    # Verifica dados do aluguel no banco
    from tinydb import Query
    Aluguel = Query()
    aluguel_salvo = db.table('alugueis').get(
        (Aluguel.ciclista == dados_aluguel_valido["ciclista"]) &
        (Aluguel.status == "EM_ANDAMENTO")
    )

    assert aluguel_salvo is not None
    assert aluguel_salvo["idBicicleta"] == mock_bicicleta_disponivel["id"]
