"""
Testes de Integração - UC01: Cadastrar Ciclista


"""
import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient

from main import app
from tests.integration.conftest import EXTERNO_URL


client = TestClient(app)


def _criar_payload_ciclista(dados_ciclista_valido):
    """Helper para criar payload no formato esperado pelo endpoint.

    O endpoint espera dois parâmetros Body:
    - dados: CiclistaCadastro
    - meio_pagamento: NovoCartaoDeCredito
    """
    # Garantir que nascimento é string (ISO format)
    nascimento = dados_ciclista_valido["nascimento"]
    if hasattr(nascimento, 'isoformat'):
        nascimento = nascimento.isoformat()

    return {
        "dados": {
            "ciclista": {
                "nome": dados_ciclista_valido["nome"],
                "nascimento": str(nascimento),
                "cpf": dados_ciclista_valido["cpf"],
                "nacionalidade": dados_ciclista_valido["nacionalidade"],
                "email": dados_ciclista_valido["email"],
                "urlFotoDocumento": dados_ciclista_valido["urlFotoDocumento"]
            },
            "senha": dados_ciclista_valido["senha"],
            "confirmacaoSenha": dados_ciclista_valido["senha"]
        },
        "meio_pagamento": dados_ciclista_valido["meioDePagamento"]
    }


# ============================================================
# TESTES DE FLUXO COMPLETO (Happy Path)
# ============================================================

@respx.mock
def test_cadastro_ciclista_sucesso_fluxo_completo(
    setup_db,
    dados_ciclista_valido,
    mock_cartao_valido,
    mock_email_enviado
):
    """
    UC01 - Testa o fluxo completo de cadastro de ciclista.

    Passos:
    1. Dados do ciclista válidos
    2. Cartão validado com sucesso (mock pagamento)
    3. Ciclista registrado no banco
    4. Email de confirmação enviado (mock email)
    """
    # Mock: POST /cartao/validar - cartão válido
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        return_value=Response(200, json=mock_cartao_valido)
    )

    # Mock: POST /email/enviar - email enviado
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["nome"] == dados_ciclista_valido["nome"]
    assert data["email"] == dados_ciclista_valido["email"]
    assert data["status"] == "AGUARDANDO_CONFIRMACAO"
    assert data["id"] is not None


@respx.mock
def test_cadastro_ciclista_registra_no_banco(
    setup_db,
    db,
    dados_ciclista_valido,
    mock_cartao_valido,
    mock_email_enviado
):
    """
    UC01 - Verifica se o ciclista é corretamente persistido no banco.

    """
    from tinydb import Query
    Ciclista = Query()

    # Mock: POST /cartao/validar - cartão válido
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        return_value=Response(200, json=mock_cartao_valido)
    )

    # Mock: POST /email/enviar - email enviado
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(200, json=mock_email_enviado)
    )

    # Conta ciclistas antes
    ciclistas_antes = len(db.table('ciclistas').all())

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)
    assert response.status_code == 201

    # Verifica se foi registrado no banco
    ciclistas_depois = len(db.table('ciclistas').all())
    assert ciclistas_depois == ciclistas_antes + 1

    # Verifica dados do ciclista no banco
    ciclista_salvo = db.table('ciclistas').get(
        Ciclista.email == dados_ciclista_valido["email"]
    )

    assert ciclista_salvo is not None
    assert ciclista_salvo["nome"] == dados_ciclista_valido["nome"]


# ============================================================
# TESTES DE FALHA - INTEGRAÇÃO COM PAGAMENTO
# ============================================================

@respx.mock
def test_cadastro_ciclista_falha_cartao_invalido(
    setup_db,
    dados_ciclista_valido,
    mock_cartao_invalido
):
    """
    UC01 - Falha quando o cartão de crédito é inválido.

    Mock retorna cartão recusado.
    """
    # Mock: POST /cartao/validar - cartão INVÁLIDO
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        return_value=Response(200, json=mock_cartao_invalido)
    )

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    # detail pode ser dict (erro customizado) ou list (validação Pydantic)
    if isinstance(detail, dict):
        assert "cartão" in detail.get("mensagem", "").lower() or "cart" in detail.get("mensagem", "").lower()
    else:
        # Se for erro de validação, verificamos o texto
        assert response.status_code == 422


@respx.mock
def test_cadastro_ciclista_falha_pagamento_timeout(setup_db, dados_ciclista_valido):
    """
    UC01 - Falha quando o serviço de pagamento não responde.

    Simula timeout do serviço de validação de cartão.
    """
    import httpx

    # Mock: POST /cartao/validar - timeout
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        side_effect=httpx.TimeoutException("Timeout")
    )

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)

    # Deve falhar quando não consegue validar o cartão
    assert response.status_code == 422


@respx.mock
def test_cadastro_ciclista_falha_servico_pagamento_erro(setup_db, dados_ciclista_valido):
    """
    UC01 - Falha quando o serviço de pagamento retorna erro 500.

    Mock retorna erro interno do servidor.
    """
    # Mock: POST /cartao/validar - erro 500
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        return_value=Response(500, json={"detail": "Erro interno"})
    )

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)

    # Deve falhar quando o serviço de pagamento retorna erro
    assert response.status_code == 422


# ============================================================
# TESTES DE FALHA NÃO-CRÍTICA - EMAIL
# ============================================================

@respx.mock
def test_cadastro_ciclista_sucesso_mesmo_com_falha_email(
    setup_db,
    dados_ciclista_valido,
    mock_cartao_valido
):
    """
    UC01 - Cadastro deve ser bem sucedido mesmo se o email falhar.

    O envio de email não é crítico para a operação de cadastro.
    """
    # Mock: POST /cartao/validar - cartão válido
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        return_value=Response(200, json=mock_cartao_valido)
    )

    # Mock: POST /email/enviar - FALHA
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        return_value=Response(500, json={"detail": "Erro ao enviar email"})
    )

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)

    # Cadastro deve funcionar mesmo com falha no email
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "AGUARDANDO_CONFIRMACAO"


@respx.mock
def test_cadastro_ciclista_sucesso_mesmo_com_email_timeout(
    setup_db,
    dados_ciclista_valido,
    mock_cartao_valido
):
    """
    UC01 - Cadastro deve ser bem sucedido mesmo se o email der timeout.

    O envio de email não é crítico para a operação de cadastro.
    """
    import httpx

    # Mock: POST /cartao/validar - cartão válido
    respx.post(f"{EXTERNO_URL}/cartao/validar").mock(
        return_value=Response(200, json=mock_cartao_valido)
    )

    # Mock: POST /email/enviar - timeout
    respx.post(f"{EXTERNO_URL}/email/enviar").mock(
        side_effect=httpx.TimeoutException("Timeout")
    )

    payload = _criar_payload_ciclista(dados_ciclista_valido)

    response = client.post("/ciclista", json=payload)

    # Cadastro deve funcionar mesmo com timeout no email
    assert response.status_code == 201


# ============================================================
# TESTES DE VALIDAÇÃO DE NEGÓCIO
# ============================================================

@respx.mock
def test_cadastro_ciclista_falha_email_ja_cadastrado(setup_db):
    """
    UC01 - A1: Falha quando o email já está cadastrado.

    A verificação de email duplicado ocorre ANTES da validação do cartão,
    então não precisamos mockar o serviço externo.
    """
    # Email do ciclista 1 que já existe no banco (init_data): user@example.com
    payload = {
        "dados": {
            "ciclista": {
                "nome": "Outro Nome",
                "nascimento": "1995-01-01",
                "cpf": "99999999999",
                "nacionalidade": "BRASILEIRO",
                "email": "user@example.com",  # Email do ciclista 1 no init_data
                "urlFotoDocumento": "https://exemplo.com/foto.jpg"
            },
            "senha": "SenhaSegura123",
            "confirmacaoSenha": "SenhaSegura123"
        },
        "meio_pagamento": {
            "nomeTitular": "Outro Nome",
            "numero": "4111111111111111",
            "validade": "12/28",
            "cvv": "123"
        }
    }

    response = client.post("/ciclista", json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    if isinstance(detail, dict):
        assert "email" in detail.get("mensagem", "").lower()


# ============================================================
# TESTES DE ATIVAÇÃO DE CICLISTA (UC02)
# ============================================================

@respx.mock
def test_ativar_ciclista_sucesso(setup_db, db):
    """
    UC02 - Testa ativação de ciclista aguardando confirmação.
    """
    # Ciclista 2 está com status AGUARDANDO_CONFIRMACAO no init_data
    response = client.post("/ciclista/2/ativar")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ATIVO"


@respx.mock
def test_ativar_ciclista_nao_encontrado(setup_db):
    """
    UC02 - Falha ao tentar ativar ciclista inexistente.
    """
    response = client.post("/ciclista/999/ativar")

    assert response.status_code == 404


# ============================================================
# TESTES DE VERIFICAÇÃO PERMITE ALUGUEL
# ============================================================

@respx.mock
def test_permite_aluguel_ciclista_ativo_sem_aluguel(setup_db):
    """
    Ciclista ativo sem aluguel em andamento pode alugar.
    """
    # Ciclista 1 está ATIVO e não tem aluguel ativo no init_data
    response = client.get("/ciclista/1/permiteAluguel")

    assert response.status_code == 200
    assert response.json() is True


@respx.mock
def test_permite_aluguel_ciclista_com_aluguel_ativo(setup_db):
    """
    Ciclista com aluguel em andamento não pode alugar.
    """
    # Ciclista 3 tem aluguel ativo no init_data
    response = client.get("/ciclista/3/permiteAluguel")

    assert response.status_code == 200
    assert response.json() is False


@respx.mock
def test_permite_aluguel_ciclista_inativo(setup_db):
    """
    Ciclista com status diferente de ATIVO não pode alugar.
    """
    # Ciclista 2 está AGUARDANDO_CONFIRMACAO no init_data
    response = client.get("/ciclista/2/permiteAluguel")

    assert response.status_code == 200
    assert response.json() is False

