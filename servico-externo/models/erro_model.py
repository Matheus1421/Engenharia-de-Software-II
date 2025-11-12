from pydantic import BaseModel, Field


class Erro(BaseModel):
    """Modelo para representar erros na API"""
    codigo: str = Field(..., description="Código do erro")
    mensagem: str = Field(..., description="Mensagem descritiva do erro")

    class Config:
        json_schema_extra = {
            "example": {
                "codigo": "404",
                "mensagem": "Recurso não encontrado"
            }
        }

