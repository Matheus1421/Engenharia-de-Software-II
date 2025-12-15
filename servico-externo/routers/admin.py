"""
Router para operações administrativas do banco de dados.
"""

from fastapi import APIRouter, Response, status
from database.database import get_db
from database.init_data import init_db

router = APIRouter(tags=["Aluguel", "Equipamento", "Externo"])


@router.get(
    "/restaurarBanco",
    summary="Restaurar dados iniciais do banco de dados do microsserviço",
)
def restaurar_banco():
    """
    Restaura o banco de dados para o estado inicial com dados de exemplo.
    Remove todos os dados existentes e insere os dados iniciais.
    """
    db = get_db()
    result = init_db(db)
    
    return {
        "mensagem": "Banco de dados restaurado com sucesso",
        "dados_inseridos": result
    }

