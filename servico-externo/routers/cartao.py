"""
Router para operações com validação de cartão de crédito.
Implementa os endpoints da API de serviços externos para validação de cartões.
"""

from typing import List, Tuple
from fastapi import APIRouter, HTTPException, status
import re

from database.database import get_db
from repositories.cartao_repository import CartaoRepository
from models.cartao_model import ValidacaoCartao, ValidarCartaoRequest
from models.erro_model import Erro


router = APIRouter(prefix="/cartao", tags=["Externo"])


def validar_cartao(numero: str, validade: str, cvv: str) -> Tuple[bool, str]:
    """
    Valida um cartão de crédito usando algoritmo de Luhn e outras validações básicas.
    
    Args:
        numero: Número do cartão
        validade: Validade no formato MM/AA
        cvv: Código CVV
        
    Returns:
        Tupla (valido, mensagem)
    """
    # Remove espaços e hífens do número
    numero_limpo = re.sub(r'[\s-]', '', numero)
    
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
        mes, ano = validade.split('/')
        mes_int = int(mes)
        ano_int = int(ano)
        
        if mes_int < 1 or mes_int > 12:
            return False, "Mês inválido na validade do cartão"
        
        # Assume que o ano é 20XX
        ano_completo = 2000 + ano_int
        from datetime import datetime
        hoje = datetime.now()
        if ano_completo < hoje.year or (ano_completo == hoje.year and mes_int < hoje.month):
            return False, "Cartão expirado"
            
    except ValueError:
        return False, "Formato de validade inválido (deve ser MM/AA)"
    
    # Valida CVV
    if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
        return False, "CVV inválido (deve ter 3 ou 4 dígitos)"
    
    return True, "Cartão válido"


@router.get("", summary="Listar validações", response_model=List[ValidacaoCartao])
def listar_validacoes():
    """
    Lista todas as validações de cartão realizadas.
    
    Returns:
        Lista de validações
    """
    db = get_db()
    cartao_repo = CartaoRepository(db)
    return cartao_repo.get_all()


@router.post("/validar", summary="Validar cartão de crédito", response_model=ValidacaoCartao, status_code=status.HTTP_200_OK)
def validar_cartao_credito(request: ValidarCartaoRequest):
    """
    Valida um cartão de crédito.
    
    Args:
        request: Dados do cartão a ser validado
        
    Returns:
        Resultado da validação
        
    Raises:
        HTTPException 422: Dados inválidos
    """
    try:
        db = get_db()
        cartao_repo = CartaoRepository(db)
        
        # Valida o cartão
        valido, mensagem = validar_cartao(
            request.numero_cartao,
            request.validade,
            request.cvv
        )
        
        # Salva a validação
        validacao = cartao_repo.create(request, valido, mensagem)
        
        return validacao
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "DADOS_INVALIDOS",
                "mensagem": str(e)
            }]
        )


@router.get("/{id_validacao}", summary="Obter validação", response_model=ValidacaoCartao)
def obter_validacao(id_validacao: int):
    """
    Obtém os dados de uma validação específica.
    
    Args:
        id_validacao: ID da validação
        
    Returns:
        Dados da validação
        
    Raises:
        HTTPException 404: Validação não encontrada
    """
    db = get_db()
    cartao_repo = CartaoRepository(db)
    validacao = cartao_repo.get_by_id(id_validacao)
    
    if not validacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "VALIDACAO_NAO_ENCONTRADA",
                "mensagem": f"Validação com ID {id_validacao} não encontrada"
            }
        )
    
    return validacao

