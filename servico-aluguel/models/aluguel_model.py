"""
MODELOS DE ALUGUEL E DEVOLUÇÃO

CASOS DE USO:
- UC03: Alugar Bicicleta
- UC04: Devolver Bicicleta

"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusAluguel(str, Enum):
    """Status do aluguel"""
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"

class StatusCobranca(str, Enum):
    """Status da cobrança"""
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
    FALHA = "FALHA"
    CANCELADA = "CANCELADA"

# MODELOS DE ALUGUEL

class NovoAluguel(BaseModel):
    """Requisição para alugar bicicleta (UC03)"""

    ciclista: int = Field(..., description="ID do ciclista")
    trancaInicio: int = Field(..., description="ID da tranca com a bicicleta")

    class Config:
        json_schema_extra = {
            "examples": [{
                "ciclista": 1,
                "trancaInicio": 1
            }]
        }

class Aluguel(BaseModel):
    """Dados completos do aluguel"""

    id: Optional[int] = Field(default=None, description="ID do aluguel")
    ciclista: int = Field(..., description="ID do ciclista")
    trancaInicio: int = Field(..., description="Tranca onde retirou a bicicleta")
    bicicleta: int = Field(..., description="ID da bicicleta alugada")
    horaInicio: datetime = Field(..., description="Data/hora do aluguel")
    trancaFim: Optional[int] = Field(default=None, description="Tranca onde devolveu")
    horaFim: Optional[datetime] = Field(default=None, description="Data/hora da devolução")
    cobranca: int = Field(..., description="ID da cobrança inicial (R$ 10,00)")
    cobrancaExtra: Optional[int] = Field(default=None, description="ID da cobrança extra (se houver)")
    status: StatusAluguel = Field(default=StatusAluguel.EM_ANDAMENTO)

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "ciclista": 1,
                "trancaInicio": 1,
                "bicicleta": 1,
                "horaInicio": "2025-11-10T10:00:00",
                "trancaFim": 2,
                "horaFim": "2025-11-10T12:30:00",
                "cobranca": 1,
                "cobrancaExtra": 2,
                "status": "FINALIZADO"
            }]
        }

# MODELOS DE DEVOLUÇÃO

class NovaDevolucao(BaseModel):
    """Requisição para devolver bicicleta (UC04)"""

    idTranca: int = Field(..., description="ID da tranca onde devolveu")
    idBicicleta: int = Field(..., description="ID da bicicleta devolvida")

    class Config:
        json_schema_extra = {
            "examples": [{
                "idTranca": 2,
                "idBicicleta": 1
            }]
        }

class Devolucao(BaseModel):
    """Resposta da devolução (dados do aluguel finalizado)"""

    aluguel: Aluguel = Field(..., description="Dados completos do aluguel")
    valorTotal: float = Field(..., description="Valor total cobrado (inicial + extra)")
    tempoTotal: int = Field(..., description="Tempo total em minutos")
    taxaExtra: float = Field(default=0.0, description="Taxa extra cobrada (se houver)")

    class Config:
        json_schema_extra = {
            "examples": [{
                "aluguel": {
                    "id": 1,
                    "ciclista": 1,
                    "bicicleta": 1,
                    "horaInicio": "2025-11-10T10:00:00",
                    "horaFim": "2025-11-10T13:45:00",
                    "cobranca": 1,
                    "cobrancaExtra": 2,
                    "status": "FINALIZADO"
                },
                "valorTotal": 25.00,
                "tempoTotal": 225,
                "taxaExtra": 15.00
            }]
        }

# MODELOS DE COBRANÇA

class NovaCobranca(BaseModel):
    """Dados para criar uma cobrança"""

    valor: float = Field(
        ...,
        gt=0,
        description="Valor a cobrar (múltiplo de 0.01)",
        examples=[10.00, 5.00, 15.50]
    )

    ciclista: int = Field(..., description="ID do ciclista a ser cobrado")

    class Config:
        json_schema_extra = {
            "examples": [{
                "valor": 10.00,
                "ciclista": 1
            }]
        }

class Cobranca(BaseModel):
    """Dados completos da cobrança"""

    id: int = Field(..., description="ID único da cobrança")
    valor: float = Field(..., description="Valor cobrado")
    ciclista: int = Field(..., description="ID do ciclista")
    status: StatusCobranca = Field(..., description="Status da cobrança")
    horaSolicitacao: datetime = Field(..., description="Quando foi solicitada")
    horaFinalizacao: Optional[datetime] = Field(default=None, description="Quando foi finalizada")
    tipo: str = Field(
        ...,
        description="Tipo da cobrança",
        examples=["ALUGUEL_INICIAL", "TAXA_EXTRA"]
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "valor": 10.00,
                "ciclista": 1,
                "status": "PAGA",
                "horaSolicitacao": "2025-11-10T10:00:00",
                "horaFinalizacao": "2025-11-10T10:00:05",
                "tipo": "ALUGUEL_INICIAL"
            }]
        }
