"""
Utilitário para tratamento padronizado de erros da API.
"""

from functools import wraps
from fastapi import HTTPException, status


def handle_api_errors(func):
    """
    Decorator para tratamento padronizado de exceções em endpoints da API.
    
    Captura exceções genéricas e as converte em HTTPException com formato padronizado,
    preservando HTTPExceptions já lançadas.
    
    Args:
        func: Função a ser decorada
        
    Returns:
        Função decorada com tratamento de erros
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            # Re-lança HTTPExceptions sem modificar
            raise
        except Exception as e:
            # Converte exceções genéricas em HTTPException padronizada
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{
                    "codigo": "DADOS_INVALIDOS",
                    "mensagem": str(e)
                }]
            )
    return wrapper
