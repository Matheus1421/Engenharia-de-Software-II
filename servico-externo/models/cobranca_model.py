from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StatusCobranca(str, Enum):
    """Status possíveis de uma cobrança"""
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"


class NovaCobranca(BaseModel):
    """Modelo para criar uma nova cobrança"""
    id_ciclista: int = Field(..., alias="idCiclista", description="ID do ciclista")
    valor: float = Field(..., description="Valor da cobrança", gt=0)
    data_vencimento: str = Field(..., alias="dataVencimento", description="Data de vencimento (ISO format)")
    descricao: str = Field(..., description="Descrição da cobrança")

    class Config:
        populate_by_name = True


class Cobranca(NovaCobranca):
    """Modelo completo de uma cobrança com ID e status"""
    id: int = Field(..., description="ID único da cobrança")
    status: StatusCobranca = Field(default=StatusCobranca.PENDENTE, description="Status atual da cobrança")
    data_criacao: str = Field(..., alias="dataCriacao", description="Data de criação (ISO format)")
    data_pagamento: Optional[str] = Field(None, alias="dataPagamento", description="Data de pagamento (ISO format)")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "idCiclista": 1,
                "valor": 50.00,
                "status": "PENDENTE",
                "dataCriacao": "2024-01-15T10:00:00Z",
                "dataVencimento": "2024-02-15T10:00:00Z",
                "dataPagamento": None,
                "descricao": "Mensalidade do mês de janeiro"
            }
        }


class ProcessarPagamentoRequest(BaseModel):
    """Modelo para processar pagamento de uma cobrança"""
    id_cobranca: int = Field(..., alias="idCobranca", description="ID da cobrança")
    id_cartao: Optional[int] = Field(None, alias="idCartao", description="ID da validação do cartão (opcional)")
    valor_pago: float = Field(..., alias="valorPago", description="Valor pago", gt=0)

    class Config:
        populate_by_name = True

