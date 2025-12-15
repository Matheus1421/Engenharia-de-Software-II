"""
Router para operações com cobranças.
Implementa os endpoints da API de serviços externos para processamento e consulta de cobranças.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone

from database.database import get_db
from repositories.cobranca_repository import CobrancaRepository
from models.cobranca_model import Cobranca, NovaCobranca, StatusCobranca


# Router apenas com as rotas do contrato externo
contrato_router = APIRouter(tags=["Externo"])


@contrato_router.post(
    "/cobranca",
    summary="Realizar cobrança",
    response_model=Cobranca,
    status_code=status.HTTP_200_OK,
)
def criar_cobranca(cobranca: NovaCobranca):
    """
    Cria uma nova cobrança no sistema conforme contrato externo.
    """
    try:
        db = get_db()
        cobranca_repo = CobrancaRepository(db)
        return cobranca_repo.create(cobranca)
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


@contrato_router.get(
    "/cobranca/{idCobranca}",
    summary="Obter cobrança",
    response_model=Cobranca,
)
def obter_cobranca(idCobranca: int):
    """
    Obtém os dados de uma cobrança específica, usando o ID informado no caminho.
    """
    db = get_db()
    cobranca_repo = CobrancaRepository(db)
    cobranca = cobranca_repo.get_by_id(idCobranca)

    if not cobranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "COBRANCA_NAO_ENCONTRADA",
                "mensagem": f"Cobrança com ID {idCobranca} não encontrada",
            },
        )

    return cobranca


@contrato_router.post(
    "/filaCobranca",
    summary=(
        "Inclui cobrança na fila de cobrança. Cobranças na fila serão "
        "cobradas de tempos em tempos."
    ),
    response_model=Cobranca,
    status_code=status.HTTP_200_OK,
)
def incluir_cobranca_na_fila(cobranca: NovaCobranca):
    """
    Inclui uma cobrança na 'fila'. No contexto atual, fila é representada
    pelas cobranças pendentes no banco.
    """
    # Reutiliza a mesma lógica de criação de cobrança
    return criar_cobranca(cobranca)


@contrato_router.post(
    "/processaCobrancasEmFila",
    summary="Processa todas as cobranças atrasadas colocadas em fila previamente.",
    response_model=List[Cobranca],
    status_code=status.HTTP_200_OK,
)
def processar_cobrancas_em_fila():
    """
    Processa todas as cobranças pendentes cujo vencimento já passou,
    marcando-as como VENCIDA.
    """
    db = get_db()
    cobranca_repo = CobrancaRepository(db)

    todas = cobranca_repo.get_all()
    agora = datetime.now(timezone.utc)
    processadas: List[Cobranca] = []

    for cobranca in todas:
        # Considera "em fila e atrasada" se está PENDENTE e data de vencimento já passou
        try:
            vencimento = datetime.fromisoformat(cobranca.data_vencimento)
        except Exception:
            # Se a data estiver em formato inesperado, ignora esta cobrança
            continue

        if cobranca.status == StatusCobranca.PENDENTE and vencimento <= agora:
            atualizada = cobranca_repo.update_status(
                cobranca.id, StatusCobranca.VENCIDA
            )
            if atualizada:
                processadas.append(atualizada)

    return processadas

