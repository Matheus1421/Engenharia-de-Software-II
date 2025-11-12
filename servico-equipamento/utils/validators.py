"""
Utilitários para validação de entidades e dados da API.
"""

from typing import Any, List
from fastapi import HTTPException, status


def validate_entity_exists(entity: Any, entity_id: int, entity_name: str) -> Any:
    """
    Valida se uma entidade existe. Se não existir, lança HTTPException 404.
    
    Args:
        entity: Entidade a ser validada (pode ser None)
        entity_id: ID da entidade buscada
        entity_name: Nome da entidade para mensagens de erro (ex: "bicicleta", "tranca")
        
    Returns:
        A própria entidade se ela existir
        
    Raises:
        HTTPException 404: Se a entidade não for encontrada
    """
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": f"{entity_name.upper()}_NAO_ENCONTRADA",
                "mensagem": f"{entity_name.capitalize()} com ID {entity_id} não encontrada"
            }
        )
    return entity


def validate_bicicleta_exists(bicicleta: Any, bicicleta_id: int) -> Any:
    """
    Valida se uma bicicleta existe. Se não existir, lança HTTPException 404.
    
    Args:
        bicicleta: Bicicleta a ser validada (pode ser None)
        bicicleta_id: ID da bicicleta buscada
        
    Returns:
        A própria bicicleta se ela existir
        
    Raises:
        HTTPException 404: Se a bicicleta não for encontrada
    """
    if not bicicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "BICICLETA_NAO_ENCONTRADA",
                "mensagem": f"Bicicleta com ID {bicicleta_id} não encontrada"
            }
        )
    return bicicleta


def validate_tranca_exists(tranca: Any, tranca_id: int) -> Any:
    """
    Valida se uma tranca existe. Se não existir, lança HTTPException 404.
    
    Args:
        tranca: Tranca a ser validada (pode ser None)
        tranca_id: ID da tranca buscada
        
    Returns:
        A própria tranca se ela existir
        
    Raises:
        HTTPException 404: Se a tranca não for encontrada
    """
    if not tranca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TRANCA_NAO_ENCONTRADA",
                "mensagem": f"Tranca com ID {tranca_id} não encontrada"
            }
        )
    return tranca


def validate_totem_exists(totem: Any, totem_id: int) -> Any:
    """
    Valida se um totem existe. Se não existir, lança HTTPException 404.
    
    Args:
        totem: Totem a ser validado (pode ser None)
        totem_id: ID do totem buscado
        
    Returns:
        O próprio totem se ele existir
        
    Raises:
        HTTPException 404: Se o totem não for encontrado
    """
    if not totem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "TOTEM_NAO_ENCONTRADO",
                "mensagem": f"Totem com ID {totem_id} não encontrado"
            }
        )
    return totem


def validate_status(status_value: str, allowed_statuses: List[str], field_name: str = "status") -> str:
    """
    Valida se um status está entre os valores permitidos.
    
    Args:
        status_value: Valor do status a ser validado
        allowed_statuses: Lista de valores permitidos
        field_name: Nome do campo para mensagens de erro
        
    Returns:
        O status em uppercase se for válido
        
    Raises:
        HTTPException 422: Se o status não for válido
    """
    status_upper = status_value.upper()
    if status_upper not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "STATUS_INVALIDO",
                "mensagem": f"{field_name} deve ser um dos seguintes: {', '.join(allowed_statuses)}"
            }]
        )
    return status_upper
