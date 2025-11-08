from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StatusBicicleta(str, Enum):
    """Status possíveis de uma bicicleta"""
    DISPONIVEL = "DISPONIVEL"
    EM_USO = "EM_USO"
    NOVA = "NOVA"
    APOSENTADA = "APOSENTADA"
    REPARO_SOLICITADO = "REPARO_SOLICITADO"
    EM_REPARO = "EM_REPARO"


class NovaBicicleta(BaseModel):
    """Modelo para criar uma nova bicicleta"""
    marca: str = Field(..., description="Marca da bicicleta")
    modelo: str = Field(..., description="Modelo da bicicleta")
    ano: str = Field(..., description="Ano de fabricação")
    numero: int = Field(..., description="Número identificador da bicicleta", gt=0)
    status: StatusBicicleta = Field(default=StatusBicicleta.NOVA, description="Status atual da bicicleta")


class Bicicleta(NovaBicicleta):
    """Modelo completo de uma bicicleta com ID"""
    id: int = Field(..., description="ID único da bicicleta")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "marca": "Caloi",
                "modelo": "Mountain Bike",
                "ano": "2023",
                "numero": 100,
                "status": "DISPONIVEL"
            }
        }
