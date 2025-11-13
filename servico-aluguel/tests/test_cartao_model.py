"""
Testes unitários de validações do modelo Cartão de Crédito.
Testa as validações básicas implementadas via Pydantic.
"""
import pytest
from pydantic import ValidationError
from models.cartao_model import NovoCartaoDeCredito, CartaoDeCredito


#   TESTES DE NOVOCARTAODECREDITO - VALIDAÇÕES

def test_cartao_numero_16_digitos_valido():
    """Testa que número de cartão com 16 dígitos é aceito"""
    cartao = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",  # 16 dígitos
        validade="12/25",
        cvv="123"
    )
    assert cartao.numero == "1234567890123456"


def test_cartao_numero_minimo_13_digitos():
    """Testa que número de cartão com 13 dígitos é aceito (mínimo)"""
    cartao = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123",  # 13 dígitos
        validade="12/25",
        cvv="123"
    )
    assert cartao.numero == "1234567890123"


def test_cartao_numero_menos_13_digitos_invalido():
    """Testa que número de cartão com menos de 13 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCartaoDeCredito(
            nomeTitular="João Silva",
            numero="123456789012",  # 12 dígitos
            validade="12/25",
            cvv="123"
        )
    assert "numero" in str(exc.value).lower()


def test_cartao_numero_mais_19_digitos_invalido():
    """Testa que número de cartão com mais de 19 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCartaoDeCredito(
            nomeTitular="João Silva",
            numero="12345678901234567890",  # 20 dígitos
            validade="12/25",
            cvv="123"
        )
    assert "numero" in str(exc.value).lower()


def test_cartao_validade_formato_correto():
    """Testa que validade no formato MM/AA é aceita"""
    cartao = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",  # MM/AA
        cvv="123"
    )
    assert cartao.validade == "12/25"


def test_cartao_validade_formato_incorreto():
    """Testa que validade em formato incorreto falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCartaoDeCredito(
            nomeTitular="João Silva",
            numero="1234567890123456",
            validade="12-25",  # Formato errado (deve ser MM/AA)
            cvv="123"
        )
    assert "validade" in str(exc.value).lower()


def test_cartao_cvv_3_digitos():
    """Testa que CVV com 3 dígitos é aceito"""
    cartao = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",
        cvv="123"
    )
    assert cartao.cvv == "123"


def test_cartao_cvv_4_digitos():
    """Testa que CVV com 4 dígitos é aceito (American Express)"""
    cartao = NovoCartaoDeCredito(
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",
        cvv="1234"
    )
    assert cartao.cvv == "1234"


def test_cartao_cvv_menos_3_digitos_invalido():
    """Testa que CVV com menos de 3 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCartaoDeCredito(
            nomeTitular="João Silva",
            numero="1234567890123456",
            validade="12/25",
            cvv="12"  # 2 dígitos
        )
    assert "cvv" in str(exc.value).lower()


def test_cartao_cvv_mais_4_digitos_invalido():
    """Testa que CVV com mais de 4 dígitos falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCartaoDeCredito(
            nomeTitular="João Silva",
            numero="1234567890123456",
            validade="12/25",
            cvv="12345"  # 5 dígitos
        )
    assert "cvv" in str(exc.value).lower()


def test_cartao_nome_titular_valido():
    """Testa que nome do titular válido é aceito"""
    cartao = NovoCartaoDeCredito(
        nomeTitular="João da Silva Santos",
        numero="1234567890123456",
        validade="12/25",
        cvv="123"
    )
    assert cartao.nomeTitular == "João da Silva Santos"


def test_cartao_nome_titular_vazio_invalido():
    """Testa que nome do titular vazio falha"""
    with pytest.raises(ValidationError) as exc:
        NovoCartaoDeCredito(
            nomeTitular="",  # Vazio
            numero="1234567890123456",
            validade="12/25",
            cvv="123"
        )
    assert "nomeTitular" in str(exc.value).lower() or "nome" in str(exc.value).lower()


#   TESTES DE CARTAODECREDITO COMPLETO

def test_cartao_completo_com_id():
    """Testa criação de CartaoDeCredito completo (com ID e idCiclista)"""
    cartao = CartaoDeCredito(
        id=1,
        nomeTitular="João Silva",
        numero="1234567890123456",
        validade="12/25",
        cvv="123",
        idCiclista=10
    )
    assert cartao.id == 1
    assert cartao.idCiclista == 10


def test_cartao_associado_a_ciclista():
    """Testa que cartão pode ser associado a um ciclista"""
    cartao = CartaoDeCredito(
        id=2,
        nomeTitular="Maria Santos",
        numero="9876543210987654",
        validade="06/26",
        cvv="456",
        idCiclista=5
    )
    assert cartao.idCiclista == 5
