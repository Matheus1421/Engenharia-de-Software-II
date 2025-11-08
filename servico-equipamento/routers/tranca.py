"""
Router para operações com trancas.
Implementa os endpoints da API de equipamentos para trancas.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from database.database import get_db
from repositories.tranca_repository import TrancaRepository
from repositories.totem_repository import TotemRepository
from repositories.bicicleta_repository import BicicletaRepository
from models.tranca_model import Tranca, NovaTranca, StatusTranca
from models.bicicleta_model import Bicicleta, StatusBicicleta
from models.erro_model import Erro


router = APIRouter(prefix="/tranca", tags=["Equipamento"])


# Modelos para requests específicos
class IntegrarNaRedeRequest(BaseModel):
    idTotem: int
    idTranca: int
    idFuncionario: int


class RetirarDaRedeRequest(BaseModel):
    idTotem: int
    idTranca: int
    idFuncionario: int
    statusAcaoReparador: str  # 'APOSENTADA' ou 'EM_REPARO'


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
    try:
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


@router.get("/{idTranca}", summary="Obter tranca", response_model=Tranca)
def obter_tranca(idTranca: int):
    """
    Obtém os dados de uma tranca específica.
    
    Args:
        idTranca: ID da tranca
        
    Returns:
        Dados da tranca
        
    Raises:
        HTTPException 404: Tranca não encontrada
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    tranca = tranca_repo.get_by_id(idTranca)
    
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {idTranca} não encontrada"
            }
        )
    
    return tranca


@router.put("/{idTranca}", summary="Editar tranca", response_model=Tranca)
def editar_tranca(idTranca: int, tranca: NovaTranca):
    """
    Atualiza os dados de uma tranca existente.
    
    Args:
        idTranca: ID da tranca
        tranca: Novos dados da tranca
        
    Returns:
        Tranca atualizada
        
    Raises:
        HTTPException 404: Tranca não encontrada
        HTTPException 422: Dados inválidos
    """
    try:
        db = get_db()
        tranca_repo = TrancaRepository(db)
        
        # Verifica se existe
        if not tranca_repo.get_by_id(idTranca):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "codigo": "TRANCA_NAO_ENCONTRADA",
                    "mensagem": f"Tranca com ID {idTranca} não encontrada"
                }
            )
        
        # Valida se o número não está sendo usado por outra tranca
        todas = tranca_repo.get_all()
        if any(t.numero == tranca.numero and t.id != idTranca for t in todas):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "NUMERO_DUPLICADO",
                    "mensagem": f"Já existe outra tranca com o número {tranca.numero}"
                }]
            )
        
        tranca_atualizada = tranca_repo.update(idTranca, tranca)
        return tranca_atualizada
        
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


@router.delete("/{idTranca}", summary="Remover tranca", status_code=status.HTTP_200_OK)
def remover_tranca(idTranca: int):
    """
    Remove uma tranca do sistema.
    
    Args:
        idTranca: ID da tranca
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 404: Tranca não encontrada
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    
    if not tranca_repo.delete(idTranca):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {idTranca} não encontrada"
            }
        )
    
    return {"mensagem": "Tranca removida com sucesso"}


@router.get("/{idTranca}/bicicleta", summary="Obter bicicleta na tranca", response_model=Bicicleta)
def obter_bicicleta_na_tranca(idTranca: int):
    """
    Obtém a bicicleta associada a uma tranca.
    
    Args:
        idTranca: ID da tranca
        
    Returns:
        Bicicleta na tranca
        
    Raises:
        HTTPException 404: Tranca ou bicicleta não encontrada
        HTTPException 422: ID da tranca inválido
    """
    # Valida ID
    if idTranca <= 0:
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
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(idTranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {idTranca} não encontrada"
            }
        )
    
    # Verifica se há bicicleta na tranca
    if not tranca.bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Não há bicicleta na tranca {idTranca}"
            }
        )
    
    # Busca bicicleta
    bicicleta = bicicleta_repo.get_by_id(tranca.bicicleta)
    if not bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta {tranca.bicicleta} não encontrada"
            }
        )
    
    return bicicleta


@router.post("/{idTranca}/trancar", summary="Trancar tranca", response_model=Tranca)
def trancar(idTranca: int, request: TrancarRequest = TrancarRequest()):
    """
    Realiza o trancamento da tranca.
    Se receber ID da bicicleta, associa a bicicleta à tranca.
    
    Args:
        idTranca: ID da tranca
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
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(idTranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {idTranca} não encontrada"
            }
        )
    
    # Verifica se a tranca já está trancada
    if tranca.status == StatusTranca.OCUPADA:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "TRANCA_JA_TRANCADA",
                "mensagem": f"A tranca {idTranca} já está trancada"
            }]
        )
    
    # Se foi fornecido ID da bicicleta, valida e associa
    if request.bicicleta:
        bicicleta = bicicleta_repo.get_by_id(request.bicicleta)
        if not bicicleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "codigo": "BICICLETA_NAO_ENCONTRADA",
                    "mensagem": f"Bicicleta com ID {request.bicicleta} não encontrada"
                }
            )
        
        # Associa bicicleta à tranca
        tranca_repo.associar_bicicleta(idTranca, request.bicicleta)
        
        # Atualiza status da bicicleta para DISPONIVEL
        bicicleta_repo.update_status(request.bicicleta, StatusBicicleta.DISPONIVEL)
    
    # Atualiza status da tranca para OCUPADA
    tranca_atualizada = tranca_repo.update_status(idTranca, StatusTranca.OCUPADA)
    
    return tranca_atualizada


@router.post("/{idTranca}/destrancar", summary="Destrancar tranca", response_model=Tranca)
def destrancar(idTranca: int, request: DestrancarRequest = DestrancarRequest()):
    """
    Realiza o destrancamento da tranca.
    Se receber ID da bicicleta, desassocia a bicicleta da tranca.
    
    Args:
        idTranca: ID da tranca
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
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(idTranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {idTranca} não encontrada"
            }
        )
    
    # Se foi fornecido ID da bicicleta, valida e desassocia
    if request.bicicleta:
        bicicleta = bicicleta_repo.get_by_id(request.bicicleta)
        if not bicicleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "codigo": "BICICLETA_NAO_ENCONTRADA",
                    "mensagem": f"Bicicleta com ID {request.bicicleta} não encontrada"
                }
            )
        
        # Verifica se a bicicleta está na tranca
        if tranca.bicicleta != request.bicicleta:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "BICICLETA_NAO_ESTA_NA_TRANCA",
                    "mensagem": f"A bicicleta {request.bicicleta} não está na tranca {idTranca}"
                }]
            )
        
        # Desassocia bicicleta da tranca
        tranca_repo.associar_bicicleta(idTranca, None)
        
        # Atualiza status da bicicleta para EM_USO
        bicicleta_repo.update_status(request.bicicleta, StatusBicicleta.EM_USO)
    
    # Atualiza status da tranca para LIVRE
    tranca_atualizada = tranca_repo.update_status(idTranca, StatusTranca.LIVRE)
    
    return tranca_atualizada


@router.post("/{idTranca}/status/{acao}", summary="Alterar status da tranca", response_model=Tranca)
def alterar_status_tranca(idTranca: int, acao: str):
    """
    Altera o status de uma tranca (TRANCAR ou DESTRANCAR).
    
    Args:
        idTranca: ID da tranca
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
    tranca = tranca_repo.get_by_id(idTranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {idTranca} não encontrada"
            }
        )
    
    # Valida a ação
    acao_upper = acao.upper()
    if acao_upper not in ["TRANCAR", "DESTRANCAR"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "ACAO_INVALIDA",
                "mensagem": f"Ação '{acao}' inválida. Valores permitidos: TRANCAR, DESTRANCAR"
            }]
        )
    
    # Define o novo status baseado na ação
    if acao_upper == "TRANCAR":
        # Verifica se já está trancada
        if tranca.status == StatusTranca.OCUPADA:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "TRANCA_JA_TRANCADA",
                    "mensagem": f"A tranca {idTranca} já está trancada"
                }]
            )
        novo_status = StatusTranca.OCUPADA
    else:  # DESTRANCAR
        novo_status = StatusTranca.LIVRE
    
    tranca_atualizada = tranca_repo.update_status(idTranca, novo_status)
    return tranca_atualizada


@router.post("/integrarNaRede", summary="Integrar tranca na rede", status_code=status.HTTP_200_OK)
def integrar_tranca_na_rede(request: IntegrarNaRedeRequest):
    """
    Coloca uma tranca nova ou retornando de reparo de volta na rede de totems.
    
    A tranca deve estar com status NOVA ou EM_REPARO.
    
    Args:
        request: Dados da integração (idTotem, idTranca, idFuncionario)
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 422: Status inválido da tranca
        HTTPException 404: Tranca ou totem não encontrado
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    totem_repo = TotemRepository(db)
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(request.idTranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {request.idTranca} não encontrada"
            }
        )
    
    # Busca totem
    totem = totem_repo.get_by_id(request.idTotem)
    if not totem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TOTEM_NAO_ENCONTRADO",
                "mensagem": f"Totem com ID {request.idTotem} não encontrado"
            }
        )
    
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
    tranca_repo.associar_totem(request.idTranca, request.idTotem)
    
    # 2. Atualiza status da tranca para LIVRE
    tranca_repo.update_status(request.idTranca, StatusTranca.LIVRE)
    
    return {
        "mensagem": "Tranca integrada na rede com sucesso",
        "idTranca": request.idTranca,
        "idTotem": request.idTotem,
        "idFuncionario": request.idFuncionario
    }


@router.post("/retirarDaRede", summary="Retirar tranca da rede", status_code=status.HTTP_200_OK)
def retirar_tranca_da_rede(request: RetirarDaRedeRequest):
    """
    Retira uma tranca para reparo ou aposentadoria.
    
    Args:
        request: Dados da retirada (idTotem, idTranca, idFuncionario, statusAcaoReparador)
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 422: Status inválido ou dados incorretos
        HTTPException 404: Tranca ou totem não encontrado
    """
    db = get_db()
    tranca_repo = TrancaRepository(db)
    totem_repo = TotemRepository(db)
    
    # Busca tranca
    tranca = tranca_repo.get_by_id(request.idTranca)
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {request.idTranca} não encontrada"
            }
        )
    
    # Busca totem
    totem = totem_repo.get_by_id(request.idTotem)
    if not totem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TOTEM_NAO_ENCONTRADO",
                "mensagem": f"Totem com ID {request.idTotem} não encontrado"
            }
        )
    
    # Verifica se a tranca está no totem
    totem_id_tranca = tranca_repo.get_totem_id(request.idTranca)
    if totem_id_tranca != request.idTotem:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "TRANCA_NAO_ESTA_NO_TOTEM",
                "mensagem": f"A tranca {request.idTranca} não está no totem {request.idTotem}"
            }]
        )
    
    # Valida o status de destino
    status_destino_upper = request.statusAcaoReparador.upper()
    if status_destino_upper not in ["APOSENTADA", "EM_REPARO"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_DESTINO_INVALIDO",
                "mensagem": "statusAcaoReparador deve ser 'APOSENTADA' ou 'EM_REPARO'"
            }]
        )
    
    # Retira da rede
    # 1. Atualiza status da tranca
    novo_status = StatusTranca.APOSENTADA if status_destino_upper == "APOSENTADA" else StatusTranca.EM_REPARO
    tranca_repo.update_status(request.idTranca, novo_status)
    
    # 2. Desassocia tranca do totem
    tranca_repo.desassociar_totem(request.idTranca)
    
    return {
        "mensagem": "Tranca retirada da rede com sucesso",
        "idTranca": request.idTranca,
        "idTotem": request.idTotem,
        "novoStatus": novo_status.value,
        "idFuncionario": request.idFuncionario
    }
