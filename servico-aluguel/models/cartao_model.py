"""
MODELOS DE CARTÃO DE CRÉDITO

CASOS DE USO:
- UC01: Cadastrar Ciclista (com cartão)
- UC07: Alterar Cartão
"""

from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

class NovoCartaoDeCredito(BaseModel):
    """Dados de cartão para cadastro/alteração"""

    nomeTitular: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome do titular (como está no cartão)",
        examples=["MARIA SILVA", "JOHN DOE"]
    )

    numero: str = Field(
        ...,
        pattern=r"^\d{13,19}$",
        description="Número do cartão (13-19 dígitos)",
        examples=["4111111111111111", "5555555555554444"]
    )

    validade: date = Field(
        ...,
        description="Data de validade (YYYY-MM-DD)",
        examples=["2028-12-31"]
    )

    cvv: str = Field(
        ...,
        pattern=r"^\d{3,4}$",
        description="Código de segurança (3 ou 4 dígitos)",
        examples=["123", "4567"]
    )

    @field_validator('validade')
    @classmethod
    def validar_validade_futura(cls, v: date) -> date:
        """Valida que o cartão não está vencido"""
        if v < date.today():
            raise ValueError("Cartão vencido")
        return v

    @field_validator('nomeTitular')
    @classmethod
    def validar_nome_maiusculo(cls, v: str) -> str:
        """Converte nome para maiúsculas (padrão de cartões)"""
        return v.upper().strip()

    class Config:
        json_schema_extra = {
            "examples": [{
                "nomeTitular": "MARIA SILVA",
                "numero": "4111111111111111",
                "validade": "2028-12-31",
                "cvv": "123"
            }]
        }

class CartaoDeCredito(BaseModel):
    """Cartão completo (com ID e relacionamento com ciclista)"""

    id: int = Field(..., description="ID único do cartão")
    idCiclista: int = Field(..., description="ID do ciclista dono do cartão")
    nomeTitular: str
    numero: str = Field(..., description="Número mascarado (ex: **** **** **** 1234)")
    validade: date
    cvv: Optional[str] = Field(default=None, exclude=True, description="NUNCA retornado")

    @classmethod
    def from_novo_cartao(cls, id: int, id_ciclista: int, cartao: NovoCartaoDeCredito):
        """Cria CartaoDeCredito a partir de NovoCartaoDeCredito com número mascarado"""
        numero_mascarado = "**** **** **** " + cartao.numero[-4:]

        return cls(
            id=id,
            idCiclista=id_ciclista,
            nomeTitular=cartao.nomeTitular,
            numero=numero_mascarado,
            validade=cartao.validade
        )

    class Config:
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "idCiclista": 1,
                "nomeTitular": "MARIA SILVA",
                "numero": "**** **** **** 1111",
                "validade": "2028-12-31"
            }]
        }
