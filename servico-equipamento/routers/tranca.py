"""
Router para operações com trancas.
Implementa os endpoints da API de equipamentos para trancas.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from enum import Enum

from database.database import get_db
from repositories.tranca_repository import TrancaRepository
from repositories.totem_repository import TotemRepository
from repositories.bicicleta_repository import BicicletaRepository
from models.tranca_model import Tranca, NovaTranca, StatusTranca
from models.bicicleta_model import Bicicleta, StatusBicicleta
from models.erro_model import Erro
from utils.error_handler import handle_api_errors
from utils.validators import validate_bicicleta_exists, validate_tranca_exists, validate_totem_exists, validate_status


router = APIRouter(prefix="/tranca", tags=["Equipamento"])


# Enum para ações de status da tranca
class AcaoTranca(str, Enum):
    """Ações possíveis para alterar status da tranca"""
    TRANCAR = "TRANCAR"
    DESTRANCAR = "DESTRANCAR"


# Modelos para requests específicos
from pydantic import Field

class IntegrarNaRedeRequest(BaseModel):
    id_totem: int = Field(..., alias='idTotem')
    id_tranca: int = Field(..., alias='idTranca')
    id_funcionario: int = Field(..., alias='idFuncionario')

    class Config:
        populate_by_name = True


class RetirarDaRedeRequest(BaseModel):
    id_totem: int = Field(..., alias='idTotem')
    id_tranca: int = Field(..., alias='idTranca')
    id_funcionario: int = Field(..., alias='idFuncionario')
    status_acao_reparador: str = Field(..., alias='statusAcaoReparador')  # 'APOSENTADA' ou 'EM_REPARO'

    class Config:
        populate_by_name = True


class TrancarRequest(BaseModel):
    bicicleta: Optional[int] = None


class DestrancarRequest(BaseModel):
    bicicleta: Optional[int] = None


@router.get("", summary="Recupera trancas cadastradas", response_model=List[Tranca])
def listar_trancas():
    """
    Lista todas as trancas cadastradas no sistema.
    
    Returns:
        Lista de trancas
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    return tranca_repo.get_all()


@router.post("", summary="Cadastrar tranca", response_model=Tranca, status_code=status.HTTP_200_OK)
@handle_api_errors
def cadastrar_tranca(tranca: NovaTranca):
    """
    Cadastra uma nova tranca no sistema.
    
    Args:
        tranca: Dados da nova tranca
        
    Returns:
        Tranca cadastrada com ID gerado
        
    Raises:
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    
    # Valida se já existe uma tranca com o mesmo número
    todas = tranca_repo.get_all()
    if any(t.numero == tranca.numero for t in todas):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "NUMERO_DUPLICADO",
                "mensagem": f"Já existe uma tranca com o número {tranca.numero}"
            }]
        )
    
    return tranca_repo.create(tranca)


@router.get("/{id_tranca}", summary="Obter tranca", response_model=Tranca)
def obter_tranca(id_tranca: int):
    """
    Obtém os dados de uma tranca específica.
    
    Args:
        id_tranca: ID da tranca
        
    Returns:
        Dados da tranca
        
    Raises:
        HTTPException 404: Tranca não encontrada
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    tranca = tranca_repo.get_by_id(id_tranca)
    
    return validate_tranca_exists(tranca, id_tranca)


@router.put("/{id_tranca}", summary="Editar tranca", response_model=Tranca)
@handle_api_errors
def editar_tranca(id_tranca: int, tranca: NovaTranca):
    """
    Atualiza os dados de uma tranca existente.
    
    Args:
        id_tranca: ID da tranca
        tranca: Novos dados da tranca
        
    Returns:
        Tranca atualizada
        
    Raises:
        HTTPException 404: Tranca não encontrada
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    
    # Verifica se existe
    validate_tranca_exists(tranca_repo.get_by_id(id_tranca), id_tranca)
    
    # Valida se o número não está sendo usado por outra tranca
    todas = tranca_repo.get_all()
    if any(t.numero == tranca.numero and t.id != id_tranca for t in todas):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "NUMERO_DUPLICADO",
                "mensagem": f"Já existe outra tranca com o número {tranca.numero}"
            }]
        )
    
    tranca_atualizada = tranca_repo.update(id_tranca, tranca)
    return tranca_atualizada


@router.delete("/{id_tranca}", summary="Remover tranca", status_code=status.HTTP_200_OK)
def remover_tranca(id_tranca: int):
    """
    Remove uma tranca do sistema.
    
    Args:
        id_tranca: ID da tranca
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 404: Tranca não encontrada
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    
    # Verifica se existe antes de remover
    validate_tranca_exists(tranca_repo.get_by_id(id_tranca), id_tranca)
    
    tranca_repo.delete(id_tranca)
    return {"mensagem": "Tranca removida com sucesso"}


@router.get("/{id_tranca}/bicicleta", summary="Obter bicicleta na tranca", response_model=Bicicleta)
def obter_bicicleta_na_tranca(id_tranca: int):
    """
    Obtém a bicicleta associada a uma tranca.
    
    Args:
        id_tranca: ID da tranca
        
    Returns:
        Bicicleta na tranca
        
    Raises:
        HTTPException 404: Tranca ou bicicleta não encontrada
        HTTPException 422: ID da tranca inválido
    """
    # Valida ID
    if id_tranca <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "codigo": "ID_INVALIDO",
                "mensagem": "O ID da tranca deve ser um número positivo"
            }
        )
    
    db = get_db()
    tranca_repo = TrancaRepository(db)
    bicicleta_repo = BicicletaRepository(db)
    
    # Busca e valida tranca
    tranca = tranca_repo.get_by_id(id_tranca)
    validate_tranca_exists(tranca, id_tranca)
    
    # Verifica se há bicicleta na tranca
    if not tranca.bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Não há bicicleta na tranca {id_tranca}"
            }
        )
    
    # Busca e valida bicicleta
    bicicleta = bicicleta_repo.get_by_id(tranca.bicicleta)
    validate_bicicleta_exists(bicicleta, tranca.bicicleta)
    
    return bicicleta


@router.post("/{id_tranca}/trancar", summary="Trancar tranca", response_model=Tranca)
def trancar(id_tranca: int, request: TrancarRequest = TrancarRequest()):
    """
    Realiza o trancamento da tranca.
    Se receber ID da bicicleta, associa a bicicleta à tranca.
    
    Args:
        id_tranca: ID da tranca
        request: Dados do trancamento (opcional: idBicicleta)
        
    Returns:
        Tranca trancada
        
    Raises:
        HTTPException 404: Tranca ou bicicleta não encontrada
        HTTPException 422: Tranca já trancada ou dados inválidos
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    bicicleta_repo = BicicletaRepository(db)
    
    # Busca e valida tranca
    tranca = tranca_repo.get_by_id(id_tranca)
    validate_tranca_exists(tranca, id_tranca)
    
    # Verifica se a tranca já está trancada
    if tranca.status == StatusTranca.OCUPADA:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "TRANCA_JA_TRANCADA",
                "mensagem": f"A tranca {id_tranca} já está trancada"
            }]
        )
    
    # Se foi fornecido ID da bicicleta, valida e associa
    if request.bicicleta:
        bicicleta = bicicleta_repo.get_by_id(request.bicicleta)
        validate_bicicleta_exists(bicicleta, request.bicicleta)
        
        # Associa bicicleta à tranca
        tranca_repo.associar_bicicleta(id_tranca, request.bicicleta)
        
        # Atualiza status da bicicleta para DISPONIVEL
        bicicleta_repo.update_status(request.bicicleta, StatusBicicleta.DISPONIVEL)
    
    # Atualiza status da tranca para OCUPADA
    tranca_atualizada = tranca_repo.update_status(id_tranca, StatusTranca.OCUPADA)
    
    return tranca_atualizada


@router.post("/{id_tranca}/destrancar", summary="Destrancar tranca", response_model=Tranca)
def destrancar(id_tranca: int, request: DestrancarRequest = DestrancarRequest()):
    """
    Realiza o destrancamento da tranca.
    Se receber ID da bicicleta, desassocia a bicicleta da tranca.
    
    Args:
        id_tranca: ID da tranca
        request: Dados do destrancamento (opcional: idBicicleta)
        
    Returns:
        Tranca destrancada
        
    Raises:
        HTTPException 404: Tranca ou bicicleta não encontrada
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    bicicleta_repo = BicicletaRepository(db)
    
    # Busca e valida tranca
    tranca = tranca_repo.get_by_id(id_tranca)
    validate_tranca_exists(tranca, id_tranca)
    
    # Se foi fornecido ID da bicicleta, valida e desassocia
    if request.bicicleta:
        bicicleta = bicicleta_repo.get_by_id(request.bicicleta)
        validate_bicicleta_exists(bicicleta, request.bicicleta)
        
        # Verifica se a bicicleta está na tranca
        if tranca.bicicleta != request.bicicleta:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "BICICLETA_NAO_ESTA_NA_TRANCA",
                    "mensagem": f"A bicicleta {request.bicicleta} não está na tranca {id_tranca}"
                }]
            )
        
        # Desassocia bicicleta da tranca
        tranca_repo.associar_bicicleta(id_tranca, None)
        
        # Atualiza status da bicicleta para EM_USO
        bicicleta_repo.update_status(request.bicicleta, StatusBicicleta.EM_USO)
    
    # Atualiza status da tranca para LIVRE
    tranca_atualizada = tranca_repo.update_status(id_tranca, StatusTranca.LIVRE)
    
    return tranca_atualizada


@router.post("/{id_tranca}/status/{acao}", summary="Alterar status da tranca", response_model=Tranca)
def alterar_status_tranca(id_tranca: int, acao: AcaoTranca):
    """
    Altera o status de uma tranca (TRANCAR ou DESTRANCAR).
    
    Args:
        id_tranca: ID da tranca
        acao: Ação a ser realizada (TRANCAR ou DESTRANCAR)
        
    Returns:
        Tranca com status atualizado
        
    Raises:
        HTTPException 404: Tranca não encontrada
        HTTPException 422: Ação inválida
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    
    # Verifica se a tranca existe
    tranca = tranca_repo.get_by_id(id_tranca)
    validate_tranca_exists(tranca, id_tranca)
    
    # O FastAPI já valida automaticamente se o valor está no Enum
    # Define o novo status baseado na ação
    if acao == AcaoTranca.TRANCAR:
        # Verifica se já está trancada
        if tranca.status == StatusTranca.OCUPADA:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "TRANCA_JA_TRANCADA",
                    "mensagem": f"A tranca {id_tranca} já está trancada"
                }]
            )
        novo_status = StatusTranca.OCUPADA
    else:  # DESTRANCAR
        novo_status = StatusTranca.LIVRE
    
    tranca_atualizada = tranca_repo.update_status(id_tranca, novo_status)
    return tranca_atualizada


@router.post("/integrarNaRede", summary="Integrar tranca na rede", status_code=status.HTTP_200_OK)
def integrar_tranca_na_rede(request: IntegrarNaRedeRequest):
    """
    Coloca uma tranca nova ou retornando de reparo de volta na rede de totems.
    
    A tranca deve estar com status NOVA ou EM_REPARO.
    
    Args:
        request: Dados da integração (idTotem, id_tranca, idFuncionario)
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 422: Status inválido da tranca
        HTTPException 404: Tranca ou totem não encontrado
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    totem_repo = TotemRepository(db)
    
    # Busca e valida tranca
    tranca = tranca_repo.get_by_id(request.id_tranca)
    validate_tranca_exists(tranca, request.id_tranca)
    
    # Busca e valida totem
    totem = totem_repo.get_by_id(request.id_totem)
    validate_totem_exists(totem, request.id_totem)
    
    # Valida status da tranca
    if tranca.status not in [StatusTranca.NOVA, StatusTranca.EM_REPARO]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_TRANCA_INVALIDO",
                "mensagem": f"Tranca deve estar com status NOVA ou EM_REPARO. Status atual: {tranca.status.value}"
            }]
        )
    
    # Integra na rede
    # 1. Associa tranca ao totem
    tranca_repo.associar_totem(request.id_tranca, request.id_totem)
    
    # 2. Atualiza status da tranca para LIVRE
    tranca_repo.update_status(request.id_tranca, StatusTranca.LIVRE)
    
    return {
        "mensagem": "Tranca integrada na rede com sucesso",
        "idTranca": request.id_tranca,
        "idTotem": request.id_totem,
        "idFuncionario": request.id_funcionario
    }


@router.post("/retirarDaRede", summary="Retirar tranca da rede", status_code=status.HTTP_200_OK)
def retirar_tranca_da_rede(request: RetirarDaRedeRequest):
    """
    Retira uma tranca para reparo ou aposentadoria.
    
    Args:
        request: Dados da retirada (idTotem, id_tranca, idFuncionario, statusAcaoReparador)
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 422: Status inválido ou dados incorretos
        HTTPException 404: Tranca ou totem não encontrado
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    totem_repo = TotemRepository(db)
    
    # Busca e valida tranca
    tranca = tranca_repo.get_by_id(request.id_tranca)
    validate_tranca_exists(tranca, request.id_tranca)
    
    # Busca e valida totem
    totem = totem_repo.get_by_id(request.id_totem)
    validate_totem_exists(totem, request.id_totem)
    
    # Verifica se a tranca está no totem
    totem_id_tranca = tranca_repo.get_totem_id(request.id_tranca)
    if totem_id_tranca != request.id_totem:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "TRANCA_NAO_ESTA_NO_TOTEM",
                "mensagem": f"A tranca {request.id_tranca} não está no totem {request.id_totem}"
            }]
        )
    
    # Valida o status de destino
    status_destino_upper = validate_status(
        request.status_acao_reparador, 
        ["APOSENTADA", "EM_REPARO"], 
        "statusAcaoReparador",
        "STATUS_DESTINO_INVALIDO"
    )
    
    # Retira da rede
    # 1. Atualiza status da tranca
    novo_status = StatusTranca.APOSENTADA if status_destino_upper == "APOSENTADA" else StatusTranca.EM_REPARO
    tranca_repo.update_status(request.id_tranca, novo_status)
    
    # 2. Desassocia tranca do totem
    tranca_repo.desassociar_totem(request.id_tranca)
    
    return {
        "mensagem": "Tranca retirada da rede com sucesso",
        "id_tranca": request.id_tranca,
        "idTotem": request.id_totem,
        "novoStatus": novo_status.value,
        "idFuncionario": request.id_funcionario
    }
