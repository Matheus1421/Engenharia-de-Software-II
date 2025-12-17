"""
MODELOS DE FUNCIONÁRIO

CASOS DE USO: UC15 (Manter Cadastro de Funcionário)
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from enum import Enum
from typing import Optional

class FuncaoFuncionario(str, Enum):
    """UC15 - R3: Função do funcionário pode ser administrativo ou reparador"""
    ADMINISTRATIVO = "ADMINISTRATIVO"
    REPARADOR = "REPARADOR"

class NovoFuncionario(BaseModel):
    """Dados para cadastro de funcionário (UC15)"""

    nome: str = Field(..., min_length=3, max_length=100)

    idade: int = Field(
        ...,
        ge=18,
        le=120,
        description="UC15 - R1: Idade >= 18 anos"
    )

    funcao: FuncaoFuncionario = Field(..., description="ADMINISTRATIVO ou REPARADOR")

    cpf: str = Field(
        ...,
        pattern=r"^\d{11}$",
        description="UC15 - R2: CPF (11 dígitos)"
    )

    email: EmailStr = Field(..., description="Email do funcionário")

    senha: str = Field(..., min_length=6, description="Senha de acesso")

    confirmacaoSenha: str = Field(..., description="Confirmação da senha")

    @model_validator(mode='after')
    def validar_senhas_iguais(self):
        """UC15 - R4: Senha e confirmação devem ser iguais"""
        if self.senha != self.confirmacaoSenha:
            raise ValueError("Senha e confirmação não conferem")
        return self

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "examples": [{
                "nome": "João Silva",
                "idade": 30,
                "funcao": "ADMINISTRATIVO",
                "cpf": "12345678901",
                "email": "joao@scb.com",
                "senha": "senha123",
                "confirmacaoSenha": "senha123"
            }]
        }

class Funcionario(BaseModel):
    """
    Funcionário completo (com matrícula gerada).

    UC15: Matrícula é gerada automaticamente e não pode ser editada
    """

    matricula: str = Field(
        ...,
        description="Matrícula única do funcionário"
    )

    nome: str
    idade: int
    funcao: FuncaoFuncionario
    cpf: str
    email: EmailStr

    # Senha não é retornada na resposta
    senha: Optional[str] = Field(default=None, exclude=True)

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "examples": [{
                "matricula": "F001",
                "nome": "Admin Sistema",
                "idade": 35,
                "funcao": "ADMINISTRATIVO",
                "cpf": "12345678901",
                "email": "admin@scb.com"
            }]
        }
