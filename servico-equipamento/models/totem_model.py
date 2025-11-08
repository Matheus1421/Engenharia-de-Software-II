from pydantic import BaseModel, Field
from typing import Optional


class NovoTotem(BaseModel):
    """Modelo para criar um novo totem"""
    localizacao: str = Field(..., description="Coordenadas de localização do totem")
    descricao: Optional[str] = Field(None, description="Descrição do totem")


class Totem(NovoTotem):
    """Modelo completo de um totem com ID"""
    id: int = Field(..., description="ID único do totem")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "localizacao": "-22.9068, -43.1729",
                "descricao": "Totem na Praça Central"
            }
        }
