"""
Router para operações com bicicletas.
Implementa os endpoints da API de equipamentos para bicicletas.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database.database import get_db
from repositories.bicicleta_repository import BicicletaRepository
from repositories.tranca_repository import TrancaRepository
from models.bicicleta_model import Bicicleta, NovaBicicleta, StatusBicicleta
from models.tranca_model import StatusTranca
from models.erro_model import Erro


router = APIRouter(prefix="/bicicleta", tags=["Equipamento"])


# Modelos para requests específicos  
from pydantic import Field

class IntegrarNaRedeRequest(BaseModel):
    id_tranca: int = Field(..., alias='idTranca')
    id_bicicleta: int = Field(..., alias='idBicicleta')
    id_funcionario: int = Field(..., alias='idFuncionario')

    class Config:
        populate_by_name = True


class RetirarDaRedeRequest(BaseModel):
    id_tranca: int = Field(..., alias='idTranca')
    id_bicicleta: int = Field(..., alias='idBicicleta')
    id_funcionario: int = Field(..., alias='idFuncionario')
    status_acao_reparador: str = Field(..., alias='statusAcaoReparador')  # 'APOSENTADA' ou 'EM_REPARO'

    class Config:
        populate_by_name = True


@router.get("", summary="Recupera bicicletas cadastradas", response_model=List[Bicicleta])
def listar_bicicletas():
    """
    Lista todas as bicicletas cadastradas no sistema.
    
    Returns:
        Lista de bicicletas
    """
    db = get_db()
    bicicleta_repo = BicicletaRepository(db)
    return bicicleta_repo.get_all()


@router.post("", summary="Cadastrar bicicleta", response_model=Bicicleta, status_code=status.HTTP_200_OK)
def cadastrar_bicicleta(bicicleta: NovaBicicleta):
    """
    Cadastra uma nova bicicleta no sistema.
    
    Args:
        bicicleta: Dados da nova bicicleta
        
    Returns:
        Bicicleta cadastrada com ID gerado
        
    Raises:
        HTTPException 422: Dados inválidos
    """
    try:
        db = get_db()
        bicicleta_repo = BicicletaRepository(db)
        
        # Valida se já existe uma bicicleta com o mesmo número
        todas = bicicleta_repo.get_all()
        if any(b.numero == bicicleta.numero for b in todas):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "NUMERO_DUPLICADO",
                    "mensagem": f"Já existe uma bicicleta com o número {bicicleta.numero}"
                }]
            )
        
        return bicicleta_repo.create(bicicleta)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "DADOS_INVALIDOS",
                "mensagem": str(e)
            }]
        )


@router.get("/{id_bicicleta}", summary="Obter bicicleta", response_model=Bicicleta)
def obter_bicicleta(id_bicicleta: int):
    """
    Obtém os dados de uma bicicleta específica.
    
    Args:
        idBicicleta: ID da bicicleta
        
    Returns:
        Dados da bicicleta
        
    Raises:
        HTTPException 404: Bicicleta não encontrada
    """
    db = get_db()
    bicicleta_repo = BicicletaRepository(db)
    bicicleta = bicicleta_repo.get_by_id(id_bicicleta)
    
    if not bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta com ID {id_bicicleta} não encontrada"
            }
        )
    
    return bicicleta


@router.put("/{id_bicicleta}", summary="Editar bicicleta", response_model=Bicicleta)
def editar_bicicleta(id_bicicleta: int, bicicleta: NovaBicicleta):
    """
    Atualiza os dados de uma bicicleta existente.
    
    Args:
        idBicicleta: ID da bicicleta
        bicicleta: Novos dados da bicicleta
        
    Returns:
        Bicicleta atualizada
        
    Raises:
        HTTPException 404: Bicicleta não encontrada
        HTTPException 422: Dados inválidos
    """
    try:
        db = get_db()
        bicicleta_repo = BicicletaRepository(db)
        
        # Verifica se existe
        if not bicicleta_repo.get_by_id(id_bicicleta):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "codigo": "BICICLETA_NAO_ENCONTRADA",
                    "mensagem": f"Bicicleta com ID {id_bicicleta} não encontrada"
                }
            )
        
        # Valida se o número não está sendo usado por outra bicicleta
        todas = bicicleta_repo.get_all()
        if any(b.numero == bicicleta.numero and b.id != id_bicicleta for b in todas):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "NUMERO_DUPLICADO",
                    "mensagem": f"Já existe outra bicicleta com o número {bicicleta.numero}"
                }]
            )
        
        bicicleta_atualizada = bicicleta_repo.update(id_bicicleta, bicicleta)
        return bicicleta_atualizada
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "DADOS_INVALIDOS",
                "mensagem": str(e)
            }]
        )


@router.delete("/{id_bicicleta}", summary="Remover bicicleta", status_code=status.HTTP_200_OK)
def remover_bicicleta(id_bicicleta: int):
    """
    Remove uma bicicleta do sistema.
    
    Args:
        idBicicleta: ID da bicicleta
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 404: Bicicleta não encontrada
    """
    db = get_db()
    bicicleta_repo = BicicletaRepository(db)
    
    if not bicicleta_repo.delete(id_bicicleta):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta com ID {id_bicicleta} não encontrada"
            }
        )
    
    return {"mensagem": "Bicicleta removida com sucesso"}


@router.post("/{id_bicicleta}/status/{acao}", summary="Alterar status da bicicleta", response_model=Bicicleta)
def alterar_status_bicicleta(id_bicicleta: int, acao: str):
    """
    Altera o status de uma bicicleta.
    
    Args:
        idBicicleta: ID da bicicleta
        acao: Novo status (DISPONIVEL, EM_USO, NOVA, APOSENTADA, REPARO_SOLICITADO, EM_REPARO)
        
    Returns:
        Bicicleta com status atualizado
        
    Raises:
        HTTPException 404: Bicicleta não encontrada
        HTTPException 422: Status inválido
    """
    db = get_db()
    bicicleta_repo = BicicletaRepository(db)
    
    # Verifica se a bicicleta existe
    if not bicicleta_repo.get_by_id(id_bicicleta):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta com ID {id_bicicleta} não encontrada"
            }
        )
    
    # Valida o status
    acao_upper = acao.upper()
    try:
        novo_status = StatusBicicleta[acao_upper]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_INVALIDO",
                "mensagem": f"Status '{acao}' inválido. Valores permitidos: DISPONIVEL, EM_USO, NOVA, APOSENTADA, REPARO_SOLICITADO, EM_REPARO"
            }]
        )
    
    bicicleta_atualizada = bicicleta_repo.update_status(id_bicicleta, novo_status)
    return bicicleta_atualizada


@router.post("/integrarNaRede", summary="Integrar bicicleta na rede de totens", status_code=status.HTTP_200_OK)
def integrar_bicicleta_na_rede(request: IntegrarNaRedeRequest):
    """
    Coloca uma bicicleta nova ou retornando de reparo de volta na rede de totens.
    
    A bicicleta deve estar com status NOVA ou EM_REPARO.
    A tranca deve estar com status LIVRE.
    
    Args:
        request: Dados da integração (idTranca, idBicicleta, idFuncionario)
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 422: Status inválido da bicicleta ou tranca
        HTTPException 404: Bicicleta ou tranca não encontrada
    """
    db = get_db()
    bicicleta_repo = BicicletaRepository(db)
    tranca_repo = TrancaRepository(db)
    
    # Busca bicicleta
    bicicleta = bicicleta_repo.get_by_id(request.id_bicicleta)
    if not bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta com ID {request.id_bicicleta} não encontrada"
            }
        )
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(request.id_tranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {request.id_tranca} não encontrada"
            }
        )
    
    # Valida status da bicicleta
    if bicicleta.status not in [StatusBicicleta.NOVA, StatusBicicleta.EM_REPARO]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_BICICLETA_INVALIDO",
                "mensagem": f"Bicicleta deve estar com status NOVA ou EM_REPARO. Status atual: {bicicleta.status.value}"
            }]
        )
    
    # Valida status da tranca
    if tranca.status != StatusTranca.LIVRE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_TRANCA_INVALIDO",
                "mensagem": f"Tranca deve estar com status LIVRE. Status atual: {tranca.status.value}"
            }]
        )
    
    # Integra na rede
    # 1. Atualiza status da bicicleta para DISPONIVEL
    bicicleta_repo.update_status(request.id_bicicleta, StatusBicicleta.DISPONIVEL)
    
    # 2. Associa bicicleta à tranca
    tranca_repo.associar_bicicleta(request.id_tranca, request.id_bicicleta)
    
    # 3. Atualiza status da tranca para OCUPADA
    tranca_repo.update_status(request.id_tranca, StatusTranca.OCUPADA)
    
    return {
        "mensagem": "Bicicleta integrada na rede com sucesso",
        "idBicicleta": request.id_bicicleta,
        "idTranca": request.id_tranca,
        "idFuncionario": request.id_funcionario
    }


@router.post("/retirarDaRede", summary="Retirar bicicleta da rede", status_code=status.HTTP_200_OK)
def retirar_bicicleta_da_rede(request: RetirarDaRedeRequest):
    """
    Retira uma bicicleta para reparo ou aposentadoria.
    
    Args:
        request: Dados da retirada (idTranca, idBicicleta, idFuncionario, statusAcaoReparador)
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 422: Status inválido ou dados incorretos
        HTTPException 404: Bicicleta ou tranca não encontrada
    """
    db = get_db()
    bicicleta_repo = BicicletaRepository(db)
    tranca_repo = TrancaRepository(db)
    
    # Busca bicicleta
    bicicleta = bicicleta_repo.get_by_id(request.id_bicicleta)
    if not bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta com ID {request.id_bicicleta} não encontrada"
            }
        )
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(request.id_tranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {request.id_tranca} não encontrada"
            }
        )
    
    # Valida se a bicicleta está na tranca
    if tranca.bicicleta != request.id_bicicleta:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "BICICLETA_NAO_ESTA_NA_TRANCA",
                "mensagem": f"A bicicleta {request.id_bicicleta} não está na tranca {request.id_tranca}"
            }]
        )
    
    # Valida o status de destino
    status_destino_upper = request.status_acao_reparador.upper()
    if status_destino_upper not in ["APOSENTADA", "EM_REPARO"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_DESTINO_INVALIDO",
                "mensagem": "statusAcaoReparador deve ser 'APOSENTADA' ou 'EM_REPARO'"
            }]
        )
    
    # Retira da rede
    # 1. Atualiza status da bicicleta
    novo_status = StatusBicicleta.APOSENTADA if status_destino_upper == "APOSENTADA" else StatusBicicleta.EM_REPARO
    bicicleta_repo.update_status(request.id_bicicleta, novo_status)
    
    # 2. Desassocia bicicleta da tranca
    tranca_repo.associar_bicicleta(request.id_tranca, None)
    
    # 3. Atualiza status da tranca para LIVRE
    tranca_repo.update_status(request.id_tranca, StatusTranca.LIVRE)
    
    return {
        "mensagem": "Bicicleta retirada da rede com sucesso",
        "idBicicleta": request.id_bicicleta,
        "idTranca": request.id_tranca,
        "novoStatus": novo_status.value,
        "idFuncionario": request.id_funcionario
    }
