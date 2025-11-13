"""
MODELOS DE CICLISTA

CASOS DE USO:
- UC01: Cadastrar Ciclista
- UC02: Confirmar Email
- UC06: Alterar Dados do Ciclista
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import date, datetime
from enum import Enum

class Nacionalidade(str, Enum):
    """Nacionalidade do ciclista"""
    BRASILEIRO = "BRASILEIRO"
    ESTRANGEIRO = "ESTRANGEIRO"

class StatusCiclista(str, Enum):
    """Status do ciclo de vida do ciclista"""
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    AGUARDANDO_CONFIRMACAO = "AGUARDANDO_CONFIRMACAO"

class Passaporte(BaseModel):
    """
    Dados do passaporte (para estrangeiros).

    UC01 - R1: Se estrangeiro, passaporte e país são obrigatórios
    """

    numero: str = Field(
        ...,
        min_length=4,
        max_length=20,
        description="Número do passaporte",
        examples=["US123456", "BR987654"]
    )

    validade: date = Field(
        ...,
        description="Data de validade do passaporte",
        examples=["2030-12-31"]
    )

    pais: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Código do país (ISO 3166-1 alpha-2)",
        examples=["BR", "US", "AR", "UY"]
    )

    @field_validator('pais')
    @classmethod
    def validar_codigo_pais(cls, v: str) -> str:
        """Valida código do país (2 letras maiúsculas)"""
        v = v.upper()
        if not v.isalpha():
            raise ValueError("Código do país deve conter apenas letras")
        return v

class NovoCiclista(BaseModel):
    """
    Dados para cadastro de novo ciclista (UC01).

    UC01 - R1 (CAMPOS OBRIGATÓRIOS):
    - Brasileiro: nome, nascimento, cpf, email, nacionalidade
    - Estrangeiro: nome, nascimento, passaporte, email, nacionalidade
    """

    nome: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome completo do ciclista",
        examples=["Maria Silva", "João Santos"]
    )

    nascimento: date = Field(
        ...,
        description="Data de nascimento (YYYY-MM-DD)",
        examples=["1995-05-10", "2000-12-25"]
    )

    cpf: Optional[str] = Field(
        default=None,
        pattern=r"^\d{11}$",
        description="UC01 - R1: CPF (11 dígitos) - Obrigatório para brasileiros",
        examples=["12345678901", "98765432100"]
    )

    passaporte: Optional[Passaporte] = Field(
        default=None,
        description="Dados do passaporte - Obrigatório para estrangeiros"
    )

    nacionalidade: Nacionalidade = Field(
        ...,
        description="Nacionalidade do ciclista"
    )

    email: EmailStr = Field(
        ...,
        description="UC01 - R3: Email do ciclista (validado via link)",
        examples=["maria@email.com", "joao@gmail.com"]
    )

    urlFotoDocumento: Optional[str] = Field(
        default=None,
        description="URL da foto do documento (CPF ou Passaporte)",
        examples=["https://exemplo.com/foto-cpf.jpg"]
    )

    @field_validator('nascimento')
    @classmethod
    def validar_data_nascimento(cls, v: date) -> date:
        """Valida que data de nascimento não é futura"""
        if v > date.today():
            raise ValueError("Data de nascimento não pode ser futura")
        return v

    @model_validator(mode='after')
    def validar_documento_obrigatorio(self):
        """
        UC01 - R1: Valida documento obrigatório conforme nacionalidade

        - Brasileiro → CPF obrigatório
        - Estrangeiro → Passaporte obrigatório
        """
        if self.nacionalidade == Nacionalidade.BRASILEIRO:
            if not self.cpf:
                raise ValueError("CPF é obrigatório para brasileiros")

        elif self.nacionalidade == Nacionalidade.ESTRANGEIRO:
            if not self.passaporte:
                raise ValueError("Passaporte é obrigatório para estrangeiros")
            if self.cpf:
                raise ValueError("Estrangeiros não podem ter CPF, apenas passaporte")

        return self

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "examples": [
                {
                    "nome": "Maria Silva",
                    "nascimento": "1995-05-10",
                    "cpf": "12345678901",
                    "passaporte": None,
                    "nacionalidade": "BRASILEIRO",
                    "email": "maria@email.com",
                    "urlFotoDocumento": "https://exemplo.com/foto.jpg"
                },
                {
                    "nome": "John Doe",
                    "nascimento": "1990-01-15",
                    "cpf": None,
                    "passaporte": {
                        "numero": "US123456",
                        "validade": "2030-12-31",
                        "pais": "US"
                    },
                    "nacionalidade": "ESTRANGEIRO",
                    "email": "john@email.com",
                    "urlFotoDocumento": "https://exemplo.com/passport.jpg"
                }
            ]
        }

class Ciclista(NovoCiclista):
    """
    Ciclista completo (após salvar no banco).

    Herda todos os campos de NovoCiclista + id, status, dataConfirmacao
    """

    id: int = Field(
        ...,
        description="ID único do ciclista (gerado automaticamente)",
        examples=[1, 2, 100]
    )

    status: StatusCiclista = Field(
        default=StatusCiclista.AGUARDANDO_CONFIRMACAO,
        description="Status atual do ciclista"
    )

    senha: Optional[str] = Field(
        default=None,
        description="Senha do ciclista (hasheada)",
        exclude=True
    )

    dataConfirmacao: Optional[datetime] = Field(
        default=None,
        description="UC02: Data/hora da confirmação do email",
        examples=["2025-11-10T14:30:00"]
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "nome": "Maria Silva",
                "nascimento": "1995-05-10",
                "cpf": "12345678901",
                "passaporte": None,
                "nacionalidade": "BRASILEIRO",
                "email": "maria@email.com",
                "urlFotoDocumento": "https://exemplo.com/foto.jpg",
                "status": "ATIVO",
                "dataConfirmacao": "2025-11-10T14:30:00"
            }]
        }

class CiclistaCadastro(BaseModel):
    """Modelo para requisição de cadastro (UC01)"""

    ciclista: NovoCiclista = Field(..., description="Dados do ciclista")

    senha: str = Field(
        ...,
        min_length=6,
        description="Senha para acesso (será hasheada)",
        examples=["senha123", "Segur@123"]
    )

    confirmacaoSenha: str = Field(
        ...,
        description="UC01 - R2: Confirmação da senha (deve ser igual)",
        examples=["senha123", "Segur@123"]
    )

    @model_validator(mode='after')
    def validar_senhas_iguais(self):
        """UC01 - R2: Senha e confirmação devem ser idênticas"""
        if self.senha != self.confirmacaoSenha:
            raise ValueError("Senha e confirmação devem ser iguais")
        return self
