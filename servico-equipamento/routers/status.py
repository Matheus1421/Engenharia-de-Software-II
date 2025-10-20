from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/status", tags=["status"])

@router.get("", summary="Status do serviço")
def get_status():
    return {
        "service": "equipamentos",
        "ok": True,
        "status": "Operacional",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

