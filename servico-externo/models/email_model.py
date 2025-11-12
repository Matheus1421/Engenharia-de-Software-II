from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class NovoEmail(BaseModel):
    """Modelo para criar um novo e-mail"""
    destinatario: EmailStr = Field(..., description="E-mail do destinatário")
    assunto: str = Field(..., description="Assunto do e-mail")
    corpo: str = Field(..., description="Corpo/conteúdo do e-mail")


class Email(NovoEmail):
    """Modelo completo de um e-mail com ID e informações de envio"""
    id: int = Field(..., description="ID único do e-mail")
    enviado: bool = Field(default=False, description="Indica se o e-mail foi enviado")
    data_envio: Optional[str] = Field(None, description="Data e hora do envio (ISO format)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "destinatario": "usuario@example.com",
                "assunto": "Bem-vindo ao Sistema",
                "corpo": "Olá! Bem-vindo ao nosso sistema.",
                "enviado": True,
                "data_envio": "2024-01-15T10:30:00Z"
            }
        }

