from pydantic import BaseModel, Field, model_serializer
from typing import Optional, Any
from enum import Enum


class StatusTranca(str, Enum):
    """Status possíveis de uma tranca"""
    LIVRE = "LIVRE"
    OCUPADA = "OCUPADA"
    NOVA = "NOVA"
    APOSENTADA = "APOSENTADA"
    EM_REPARO = "EM_REPARO"
    REPARO_SOLICITADO = "REPARO_SOLICITADO"


class NovaTranca(BaseModel):
    """Modelo para criar uma nova tranca"""
    numero: int = Field(..., description="Número identificador da tranca", gt=0)
    localizacao: str = Field(..., description="Coordenadas de localização")
    anoDeFabricacao: str = Field(..., description="Ano de fabricação da tranca")
    modelo: str = Field(..., description="Modelo da tranca")
    status: StatusTranca = Field(default=StatusTranca.NOVA, description="Status atual da tranca")


class Tranca(NovaTranca):
    """Modelo completo de uma tranca com ID"""
    id: int = Field(..., description="ID único da tranca")
    bicicleta: Optional[int] = Field(None, description="ID da bicicleta associada à tranca")
    totem: Optional[int] = Field(None, description="ID do totem associado à tranca")

    @model_serializer(mode='wrap')
    def serialize_model(self, handler: Any) -> dict:
        """Adiciona bicicleta_id como alias de bicicleta na serialização"""
        data = handler(self)
        data['bicicleta_id'] = data.get('bicicleta')
        return data

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "numero": 1,
                "localizacao": "-22.9068, -43.1729",
                "anoDeFabricacao": "2023",
                "modelo": "Tranca Modelo X",
                "status": "LIVRE",
                "bicicleta": None,
                "bicicleta_id": None,
                "totem": 1
            }
        }
