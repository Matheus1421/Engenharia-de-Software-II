from pydantic import BaseModel, Field
from typing import Optional


class ValidarCartaoRequest(BaseModel):
    """Modelo para validar um cartão de crédito"""
    numero_cartao: str = Field(..., alias="numeroCartao", description="Número do cartão de crédito", min_length=13, max_length=19)
    nome_portador: str = Field(..., alias="nomePortador", description="Nome do portador do cartão")
    validade: str = Field(..., description="Validade do cartão (MM/AA)", pattern=r"^\d{2}/\d{2}$")
    cvv: str = Field(..., description="Código de segurança (CVV)", min_length=3, max_length=4)

    class Config:
        populate_by_name = True


class ValidacaoCartao(BaseModel):
    """Modelo completo de uma validação de cartão"""
    id: int = Field(..., description="ID único da validação")
    numero_cartao: str = Field(..., alias="numeroCartao", description="Número do cartão (mascarado)")
    nome_portador: str = Field(..., alias="nomePortador", description="Nome do portador do cartão")
    validade: str = Field(..., description="Validade do cartão")
    cvv: str = Field(..., description="Código de segurança (CVV)")
    valido: bool = Field(..., description="Indica se o cartão é válido")
    data_validacao: str = Field(..., alias="dataValidacao", description="Data da validação (ISO format)")
    mensagem: str = Field(..., description="Mensagem descritiva da validação")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "numeroCartao": "4111********1111",
                "nomePortador": "João Silva",
                "validade": "12/25",
                "cvv": "123",
                "valido": True,
                "dataValidacao": "2024-01-15T11:00:00Z",
                "mensagem": "Cartão válido"
            }
        }

