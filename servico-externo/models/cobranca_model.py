from pydantic import BaseModel, Field, model_serializer
from typing import Optional, Any
from enum import Enum


class StatusCobranca(str, Enum):
    """Status possíveis de uma cobrança"""
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
    FALHA = "FALHA"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"


class NovaCobranca(BaseModel):
    """Modelo para criar uma nova cobrança - compatível com Postman e servico-aluguel"""
    # Aceita tanto "ciclista" quanto "idCiclista"
    ciclista: int = Field(..., alias="ciclista", description="ID do ciclista")
    valor: float = Field(..., description="Valor da cobrança", gt=0)
    # Campos opcionais para compatibilidade com servico-aluguel
    status: Optional[str] = Field(None, description="Status da cobrança (opcional)")
    horaSolicitacao: Optional[str] = Field(None, description="Hora da solicitação (ISO format)")
    horaFinalizacao: Optional[str] = Field(None, description="Hora da finalização (ISO format)")

    class Config:
        populate_by_name = True


class Cobranca(BaseModel):
    """Modelo completo de uma cobrança - retorna campos esperados pelo Postman"""
    id: int = Field(..., description="ID único da cobrança")
    ciclista: int = Field(..., description="ID do ciclista")
    valor: float = Field(..., description="Valor da cobrança")
    status: str = Field(..., description="Status atual da cobrança")
    horaSolicitacao: str = Field(..., description="Hora da solicitação (ISO format)")
    horaFinalizacao: Optional[str] = Field(None, description="Hora da finalização (ISO format)")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "ciclista": 1,
                "valor": 100.00,
                "status": "PAGA",
                "horaSolicitacao": "2024-01-15T10:00:00Z",
                "horaFinalizacao": "2024-01-15T10:00:05Z"
            }
        }


class ProcessarPagamentoRequest(BaseModel):
    """Modelo para processar pagamento de uma cobrança"""
    id_cobranca: int = Field(..., alias="idCobranca", description="ID da cobrança")
    id_cartao: Optional[int] = Field(None, alias="idCartao", description="ID da validação do cartão (opcional)")
    valor_pago: float = Field(..., alias="valorPago", description="Valor pago", gt=0)

    class Config:
        populate_by_name = True

