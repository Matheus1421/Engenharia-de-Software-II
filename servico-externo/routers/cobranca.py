"""
Router para operações com cobranças.
Implementa os endpoints da API de serviços externos para processamento e consulta de cobranças.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone

from database.database import get_db
from repositories.cobranca_repository import CobrancaRepository
from models.cobranca_model import Cobranca, NovaCobranca, StatusCobranca, ProcessarPagamentoRequest
from models.erro_model import Erro


router = APIRouter(prefix="/cobranca", tags=["Externo"])


@router.get("", summary="Listar cobranças", response_model=List[Cobranca])
def listar_cobrancas():
    """
    Lista todas as cobranças cadastradas no sistema.
    
    Returns:
        Lista de cobranças
    """
    db = get_db()
    cobranca_repo = CobrancaRepository(db)
    return cobranca_repo.get_all()


@router.post("", summary="Criar cobrança", response_model=Cobranca, status_code=status.HTTP_200_OK)
def criar_cobranca(cobranca: NovaCobranca):
    """
    Cria uma nova cobrança no sistema.
    
    Args:
        cobranca: Dados da nova cobrança
        
    Returns:
        Cobrança criada com ID gerado
        
    Raises:
        HTTPException 422: Dados inválidos
    """
    try:
        db = get_db()
        cobranca_repo = CobrancaRepository(db)
        
        return cobranca_repo.create(cobranca)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "DADOS_INVALIDOS",
                "mensagem": str(e)
            }]
        )


@router.get("/{id_cobranca}", summary="Obter cobrança", response_model=Cobranca)
def obter_cobranca(id_cobranca: int):
    """
    Obtém os dados de uma cobrança específica.
    
    Args:
        id_cobranca: ID da cobrança
        
    Returns:
        Dados da cobrança
        
    Raises:
        HTTPException 404: Cobrança não encontrada
    """
    db = get_db()
    cobranca_repo = CobrancaRepository(db)
    cobranca = cobranca_repo.get_by_id(id_cobranca)
    
    if not cobranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "COBRANCA_NAO_ENCONTRADA",
                "mensagem": f"Cobrança com ID {id_cobranca} não encontrada"
            }
        )
    
    return cobranca


@router.get("/{id_cobranca}/status", summary="Consultar status da cobrança", response_model=Cobranca)
def consultar_status_cobranca(id_cobranca: int):
    """
    Consulta o status atual de uma cobrança.
    
    Args:
        id_cobranca: ID da cobrança
        
    Returns:
        Dados da cobrança com status atual
        
    Raises:
        HTTPException 404: Cobrança não encontrada
    """
    db = get_db()
    cobranca_repo = CobrancaRepository(db)
    cobranca = cobranca_repo.get_by_id(id_cobranca)
    
    if not cobranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "COBRANCA_NAO_ENCONTRADA",
                "mensagem": f"Cobrança com ID {id_cobranca} não encontrada"
            }
        )
    
    return cobranca


@router.post("/{id_cobranca}/processar", summary="Processar pagamento", response_model=Cobranca, status_code=status.HTTP_200_OK)
def processar_pagamento(id_cobranca: int, request: ProcessarPagamentoRequest):
    """
    Processa o pagamento de uma cobrança.
    
    Args:
        id_cobranca: ID da cobrança
        request: Dados do pagamento
        
    Returns:
        Cobrança atualizada com status PAGA
        
    Raises:
        HTTPException 404: Cobrança não encontrada
        HTTPException 422: Dados inválidos ou valor incorreto
    """
    db = get_db()
    cobranca_repo = CobrancaRepository(db)
    
    # Verifica se a cobrança existe
    cobranca = cobranca_repo.get_by_id(id_cobranca)
    if not cobranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "COBRANCA_NAO_ENCONTRADA",
                "mensagem": f"Cobrança com ID {id_cobranca} não encontrada"
            }
        )
    
    # Valida se o ID da cobrança no request corresponde ao da URL
    if request.id_cobranca != id_cobranca:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "ID_INCONSISTENTE",
                "mensagem": "O ID da cobrança no request deve corresponder ao ID da URL"
            }]
        )
    
    # Valida o valor pago
    if abs(request.valor_pago - cobranca.valor) > 0.01:  # Permite pequena diferença de arredondamento
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "VALOR_INCORRETO",
                "mensagem": f"O valor pago (R$ {request.valor_pago:.2f}) não corresponde ao valor da cobrança (R$ {cobranca.valor:.2f})"
            }]
        )
    
    # Verifica se já está paga
    if cobranca.status == StatusCobranca.PAGA:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "COBRANCA_JA_PAGA",
                "mensagem": "Esta cobrança já foi paga"
            }]
        )
    
    # Processa o pagamento
    cobranca_atualizada = cobranca_repo.update_status(id_cobranca, StatusCobranca.PAGA)
    
    return cobranca_atualizada

