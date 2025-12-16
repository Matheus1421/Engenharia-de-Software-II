"""Modelo para registros de auditoria do sistema."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TipoAcao(str, Enum):
    """Tipos de ação que podem ser auditadas"""
    # Bicicletas
    INTEGRAR_BICICLETA = "INTEGRAR_BICICLETA"  # UC08
    RETIRAR_BICICLETA = "RETIRAR_BICICLETA"    # UC09
    
    # Trancas
    INTEGRAR_TRANCA = "INTEGRAR_TRANCA"        # UC11
    RETIRAR_TRANCA = "RETIRAR_TRANCA"          # UC12


class TipoEquipamento(str, Enum):
    """Tipo de equipamento sendo auditado"""
    BICICLETA = "BICICLETA"
    TRANCA = "TRANCA"


class RegistroAuditoria(BaseModel):
    """Modelo base para criar um registro de auditoria"""
    tipo_acao: TipoAcao = Field(..., description="Tipo de ação realizada")
    tipo_equipamento: TipoEquipamento = Field(..., description="Tipo de equipamento")
    id_equipamento: int = Field(..., description="ID do equipamento (bicicleta ou tranca)")
    numero_equipamento: int = Field(..., description="Número identificador do equipamento")
    id_funcionario: int = Field(..., description="ID do funcionário/reparador que realizou a ação")
    id_tranca: Optional[int] = Field(None, description="ID da tranca relacionada (para bicicletas)")
    id_totem: Optional[int] = Field(None, description="ID do totem relacionado (para trancas)")
    status_destino: Optional[str] = Field(None, description="Status de destino (APOSENTADA, EM_REPARO, DISPONIVEL, etc)")
    detalhes: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detalhes adicionais da operação")
    data_hora: datetime = Field(default_factory=datetime.now, description="Data e hora da ação")


class RegistroAuditoriaCompleto(RegistroAuditoria):
    """Modelo completo de auditoria com ID"""
    id: int = Field(..., description="ID único do registro de auditoria")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "tipo_acao": "RETIRAR_BICICLETA",
                "tipo_equipamento": "BICICLETA",
                "id_equipamento": 10,
                "numero_equipamento": 100,
                "id_funcionario": 5,
                "id_tranca": 3,
                "id_totem": None,
                "status_destino": "EM_REPARO",
                "detalhes": {
                    "motivo": "Manutenção preventiva",
                    "observacoes": "Freio necessita ajuste"
                },
                "data_hora": "2024-01-15T14:30:00"
            }
        }
