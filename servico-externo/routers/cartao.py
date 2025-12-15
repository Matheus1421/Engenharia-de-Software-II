"""
Router para operações com validação de cartão de crédito,
expondo apenas a rota do contrato externo.
"""

from typing import Tuple
from fastapi import APIRouter, HTTPException, status
import re

from database.database import get_db
from repositories.cartao_repository import CartaoRepository
from models.cartao_model import ValidacaoCartao, ValidarCartaoRequest


contrato_router = APIRouter(tags=["Externo"])


def validar_cartao(numero: str, validade: str, cvv: str) -> Tuple[bool, str]:
    """
    Valida um cartão de crédito usando algoritmo de Luhn e outras validações básicas.
    """
    # Remove espaços e hífens do número
    numero_limpo = re.sub(r"[\s-]", "", numero)

    # Valida se contém apenas dígitos
    if not numero_limpo.isdigit():
        return False, "Número do cartão deve conter apenas dígitos"

    # Valida comprimento (13-19 dígitos)
    if len(numero_limpo) < 13 or len(numero_limpo) > 19:
        return False, "Número do cartão deve ter entre 13 e 19 dígitos"

    # Algoritmo de Luhn
    def luhn_check(card_number: str) -> bool:
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0

    if not luhn_check(numero_limpo):
        return False, "Número do cartão inválido (falha no algoritmo de Luhn)"

    # Valida validade (formato MM/AA)
    try:
        mes, ano = validade.split("/")
        mes_int = int(mes)
        ano_int = int(ano)

        if mes_int < 1 or mes_int > 12:
            return False, "Mês inválido na validade do cartão"

        # Assume que o ano é 20XX
        from datetime import datetime

        ano_completo = 2000 + ano_int
        hoje = datetime.now()
        if ano_completo < hoje.year or (ano_completo == hoje.year and mes_int < hoje.month):
            return False, "Cartão expirado"

    except ValueError:
        return False, "Formato de validade inválido (deve ser MM/AA)"

    # Valida CVV
    if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
        return False, "CVV inválido (deve ter 3 ou 4 dígitos)"

    return True, "Cartão válido"


@contrato_router.post(
    "/validaCartaoDeCredito",
    summary="Valida um cartão de crédito",
    response_model=ValidacaoCartao,
    status_code=status.HTTP_200_OK,
)
def valida_cartao_de_credito(request: ValidarCartaoRequest):
    """
    Endpoint de alto nível para validação de cartão de crédito,
    conforme contrato externo.
    """
    try:
        db = get_db()
        cartao_repo = CartaoRepository(db)

        valido, mensagem = validar_cartao(
            request.numero_cartao,
            request.validade,
            request.cvv,
        )

        validacao = cartao_repo.create(request, valido, mensagem)
        return validacao

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "codigo": "DADOS_INVALIDOS",
                    "mensagem": str(e),
                }
            ],
        )

