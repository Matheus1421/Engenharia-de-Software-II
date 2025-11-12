"""
Router para operações com e-mails.
Implementa os endpoints da API de serviços externos para notificações por e-mail.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone

from database.database import get_db
from repositories.email_repository import EmailRepository
from models.email_model import Email, NovoEmail
from models.erro_model import Erro
from services.email_service import email_service


router = APIRouter(prefix="/email", tags=["Externo"])


@router.get("", summary="Listar e-mails", response_model=List[Email])
def listar_emails():
    """
    Lista todos os e-mails cadastrados no sistema.
    
    Returns:
        Lista de e-mails
    """
    db = get_db()
    email_repo = EmailRepository(db)
    return email_repo.get_all()


@router.post("/enviar", summary="Enviar e-mail", response_model=Email, status_code=status.HTTP_200_OK)
def enviar_email(email: NovoEmail):
    """
    Envia um novo e-mail via SMTP.
    
    Args:
        email: Dados do e-mail a ser enviado
        
    Returns:
        E-mail criado e marcado como enviado
        
    Raises:
        HTTPException 422: Dados inválidos
        HTTPException 500: Erro ao enviar e-mail
    """
    try:
        db = get_db()
        email_repo = EmailRepository(db)
        
        # Cria o e-mail no banco de dados
        novo_email = email_repo.create(email)
        
        # Envia o e-mail via SMTP
        sucesso, erro = email_service.enviar_email(
            destinatario=email.destinatario,
            assunto=email.assunto,
            corpo=email.corpo
        )
        
        if not sucesso:
            # Se falhar, mantém o e-mail como não enviado
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=[{
                    "codigo": "ERRO_ENVIO_EMAIL",
                    "mensagem": f"Erro ao enviar e-mail: {erro or 'Erro desconhecido'}"
                }]
            )
        
        # Marca como enviado após sucesso
        email_enviado = email_repo.marcar_como_enviado(novo_email.id)
        
        return email_enviado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "codigo": "DADOS_INVALIDOS",
                "mensagem": str(e)
            }]
        )


@router.get("/{id_email}", summary="Obter e-mail", response_model=Email)
def obter_email(id_email: int):
    """
    Obtém os dados de um e-mail específico.
    
    Args:
        id_email: ID do e-mail
        
    Returns:
        Dados do e-mail
        
    Raises:
        HTTPException 404: E-mail não encontrado
    """
    db = get_db()
    email_repo = EmailRepository(db)
    email = email_repo.get_by_id(id_email)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "codigo": "EMAIL_NAO_ENCONTRADO",
                "mensagem": f"E-mail com ID {id_email} não encontrado"
            }
        )
    
    return email

