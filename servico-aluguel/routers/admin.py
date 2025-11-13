"""ROUTER: Admin"""
from fastapi import APIRouter
from database.database import get_db, reset_db
from database.init_data import init_db

router = APIRouter(prefix="", tags=["Admin"])

@router.get("/restaurarBanco")
def restaurar_banco():
    """
    Restaura banco de dados ao estado inicial.

    """
    reset_db()
    db = get_db()
    init_db(db)

    return {
        "status": "success",
        "message": "Banco de dados restaurado com dados iniciais"
    }
