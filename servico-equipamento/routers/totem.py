"""
Router para operações com totems.
Implementa os endpoints da API de equipamentos para totems.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from database.database import get_db
from repositories.totem_repository import TotemRepository
from repositories.tranca_repository import TrancaRepository
from repositories.bicicleta_repository import BicicletaRepository
from models.totem_model import Totem, NovoTotem
from models.tranca_model import Tranca
from models.bicicleta_model import Bicicleta
from models.erro_model import Erro
from utils.error_handler import handle_api_errors
from utils.validators import validate_totem_exists


router = APIRouter(prefix="/totem", tags=["Equipamento"])


@router.get("", summary="Recupera totens cadastrados", response_model=List[Totem])
def listar_totems():
    """
    Lista todos os totems cadastrados no sistema.
    
    Returns:
        Lista de totems
    """
    db = get_db()
    totem_repo = TotemRepository(db)
    return totem_repo.get_all()


@router.post("", summary="Incluir totem", response_model=Totem, status_code=status.HTTP_200_OK)
@handle_api_errors
def cadastrar_totem(totem: NovoTotem):
    """
    Cadastra um novo totem no sistema.
    
    Args:
        totem: Dados do novo totem
        
    Returns:
        Totem cadastrado com ID gerado
        
    Raises:
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    totem_repo = TotemRepository(db)
    
    # Valida se a localização não está vazia
    if not totem.localizacao or totem.localizacao.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "LOCALIZACAO_INVALIDA",
                "mensagem": "A localização do totem é obrigatória"
            }]
        )
    
    return totem_repo.create(totem)


@router.put("/{id_totem}", summary="Editar totem", response_model=Totem)
@handle_api_errors
def editar_totem(id_totem: int, totem: NovoTotem):
    """
    Atualiza os dados de um totem existente.
    
    Args:
        id_totem: ID do totem
        totem: Novos dados do totem
        
    Returns:
        Totem atualizado
        
    Raises:
        HTTPException 404: Totem não encontrado
        HTTPException 422: Dados inválidos
    """
    db = get_db()
    totem_repo = TotemRepository(db)
    
    # Verifica se existe
    validate_totem_exists(totem_repo.get_by_id(id_totem), id_totem)
    
    # Valida se a localização não está vazia
    if not totem.localizacao or totem.localizacao.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "LOCALIZACAO_INVALIDA",
                "mensagem": "A localização do totem é obrigatória"
            }]
        )
    
    totem_atualizado = totem_repo.update(id_totem, totem)
    return totem_atualizado


@router.delete("/{id_totem}", summary="Remover totem", status_code=status.HTTP_200_OK)
def remover_totem(id_totem: int):
    """
    Remove um totem do sistema.
    
    Args:
        id_totem: ID do totem
        
    Returns:
        Mensagem de sucesso
        
    Raises:
        HTTPException 404: Totem não encontrado
    """
    db = get_db()
    totem_repo = TotemRepository(db)
    
    # Verifica se o totem existe
    validate_totem_exists(totem_repo.get_by_id(id_totem), id_totem)
    
    # Remove o totem (o repositório já remove as associações com trancas)
    totem_repo.delete(id_totem)
    
    return {"mensagem": "Totem removido com sucesso"}


@router.get("/{id_totem}/trancas", summary="Listar trancas de um totem", response_model=List[Tranca])
def listar_trancas_do_totem(id_totem: int):
    """
    Lista todas as trancas associadas a um totem.
    
    Args:
        id_totem: ID do totem
        
    Returns:
        Lista de trancas do totem
        
    Raises:
        HTTPException 404: Totem não encontrado
        HTTPException 422: ID do totem inválido
    """
    # Valida o ID
    if id_totem <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "ID_INVALIDO",
                "mensagem": "O ID do totem deve ser um número positivo"
            }]
        )
    
    db = get_db()
    totem_repo = TotemRepository(db)
    tranca_repo = TrancaRepository(db)
    
    # Verifica se o totem existe
    validate_totem_exists(totem_repo.get_by_id(id_totem), id_totem)
    
    # Busca os IDs das trancas associadas ao totem
    trancas_ids = totem_repo.get_trancas_ids(id_totem)
    
    # Busca os dados completos de cada tranca
    trancas = []
    for tranca_id in trancas_ids:
        tranca = tranca_repo.get_by_id(tranca_id)
        if tranca:
            trancas.append(tranca)
    
    return trancas


@router.get("/{id_totem}/bicicletas", summary="Listar bicicletas de um totem", response_model=List[Bicicleta])
def listar_bicicletas_do_totem(id_totem: int):
    """
    Lista todas as bicicletas associadas às trancas de um totem.
    
    Args:
        id_totem: ID do totem
        
    Returns:
        Lista de bicicletas no totem
        
    Raises:
        HTTPException 404: Totem não encontrado
        HTTPException 422: ID do totem inválido
    """
    # Valida o ID
    if id_totem <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "ID_INVALIDO",
                "mensagem": "O ID do totem deve ser um número positivo"
            }]
        )
    
    db = get_db()
    totem_repo = TotemRepository(db)
    tranca_repo = TrancaRepository(db)
    bicicleta_repo = BicicletaRepository(db)
    
    # Verifica se o totem existe
    validate_totem_exists(totem_repo.get_by_id(id_totem), id_totem)
    
    # Busca os IDs das trancas associadas ao totem
    trancas_ids = totem_repo.get_trancas_ids(id_totem)
    
    # Busca as bicicletas associadas a cada tranca
    bicicletas = []
    bicicletas_ids_processados = set()  # Para evitar duplicatas
    
    for tranca_id in trancas_ids:
        tranca = tranca_repo.get_by_id(tranca_id)
        if tranca and tranca.bicicleta:
            # Evita adicionar a mesma bicicleta duas vezes
            if tranca.bicicleta not in bicicletas_ids_processados:
                bicicleta = bicicleta_repo.get_by_id(tranca.bicicleta)
                if bicicleta:
                    bicicletas.append(bicicleta)
                    bicicletas_ids_processados.add(tranca.bicicleta)
    
    return bicicletas
