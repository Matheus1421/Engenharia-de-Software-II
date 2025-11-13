"""
MODELO DE ERRO - PADRONIZAÇÃO DE RESPOSTAS DE ERRO

RESPONSABILIDADE: Definir estrutura padrão para mensagens de erro da API
"""

from pydantic import BaseModel, Field
from typing import Optional

class Erro(BaseModel):
    """Modelo de erro conforme especificação da API"""

    codigo: str = Field(
        ...,
        description="Código único do erro (ex: EMAIL_JA_CADASTRADO)",
        examples=["EMAIL_JA_CADASTRADO", "DADOS_INVALIDOS", "NAO_ENCONTRADO"]
    )

    mensagem: str = Field(
        ...,
        description="Mensagem descritiva do erro para o usuário",
        examples=[
            "O email já está cadastrado",
            "CPF inválido",
            "Ciclista não encontrado"
        ]
    )

    detalhes: Optional[str] = Field(
        default=None,
        description="Informações técnicas adicionais (opcional)",
        examples=["ValidationError: field 'cpf' invalid"]
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "codigo": "EMAIL_JA_CADASTRADO",
                    "mensagem": "O email informado já está cadastrado no sistema",
                    "detalhes": None
                },
                {
                    "codigo": "CARTAO_INVALIDO",
                    "mensagem": "O cartão de crédito foi recusado pela operadora",
                    "detalhes": "Invalid card number"
                }
            ]
        }

class CodigosErro:
    """Constantes para códigos de erro (evita erros de digitação)"""

    # Erros de Ciclista
    EMAIL_JA_CADASTRADO = "EMAIL_JA_CADASTRADO"
    EMAIL_INVALIDO = "EMAIL_INVALIDO"
    CICLISTA_NAO_ENCONTRADO = "CICLISTA_NAO_ENCONTRADO"
    CICLISTA_INATIVO = "CICLISTA_INATIVO"
    CICLISTA_JA_TEM_ALUGUEL = "CICLISTA_JA_TEM_ALUGUEL"

    # Erros de Cartão
    CARTAO_INVALIDO = "CARTAO_INVALIDO"
    CARTAO_RECUSADO = "CARTAO_RECUSADO"
    CARTAO_NAO_ENCONTRADO = "CARTAO_NAO_ENCONTRADO"

    # Erros de Funcionário
    FUNCIONARIO_NAO_ENCONTRADO = "FUNCIONARIO_NAO_ENCONTRADO"
    MATRICULA_JA_EXISTE = "MATRICULA_JA_EXISTE"

    # Erros de Aluguel
    TRANCA_INVALIDA = "TRANCA_INVALIDA"
    TRANCA_SEM_BICICLETA = "TRANCA_SEM_BICICLETA"
    BICICLETA_NAO_DISPONIVEL = "BICICLETA_NAO_DISPONIVEL"
    BICICLETA_NAO_ENCONTRADA = "BICICLETA_NAO_ENCONTRADA"

    # Erros de Cobrança
    PAGAMENTO_RECUSADO = "PAGAMENTO_RECUSADO"
    COBRANCA_FALHOU = "COBRANCA_FALHOU"

    # Erros Genéricos
    DADOS_INVALIDOS = "DADOS_INVALIDOS"
    ERRO_INTERNO = "ERRO_INTERNO"
    NAO_ENCONTRADO = "NAO_ENCONTRADO"
    REQUISICAO_MAL_FORMADA = "REQUISICAO_MAL_FORMADA"
