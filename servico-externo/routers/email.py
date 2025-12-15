"""
Router para operações com e-mails.
Implementa os endpoints da API de serviços externos para notificações por e-mail.
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status, Body

from database.database import get_db
from repositories.email_repository import EmailRepository
from models.email_model import Email, NovoEmail
from services.email_service import email_service
from typing import Union


# Router apenas com as rotas do contrato externo
contrato_router = APIRouter(tags=["Externo"])


@contrato_router.post(
    "/enviarEmail",
    summary="Notificar via email",
    response_model=Email,
    status_code=status.HTTP_200_OK,
)
def enviar_email_contrato(
    payload: Union[NovoEmail,Dict[str, Any]] = Body(...)
    ):
    """
    Endpoint de alto nível para envio de e-mail conforme o contrato.

    Compatível com dois formatos de payload:
    - Formato antigo: {\"destinatario\", \"assunto\", \"corpo\"}
    - Formato novo (utilizado pelos outros microsserviços): {\"email\", \"assunto\", \"mensagem\"}
    """
    # Normaliza o payload para o modelo NovoEmail esperado internamente
    if "destinatario" in payload or "corpo" in payload:
        dados_email = payload
    else:
        dados_email = {
            "destinatario": payload.get("email"),
            "assunto": payload.get("assunto"),
            "corpo": payload.get("mensagem"),
        }

    try:
        email_model = NovoEmail(**dados_email)

        db = get_db()
        email_repo = EmailRepository(db)

        # Cria o e-mail no banco de dados
        novo_email = email_repo.create(email_model)

        # Envia o e-mail via SMTP
        sucesso, erro = email_service.enviar_email(
            destinatario=email_model.destinatario,
            assunto=email_model.assunto,
            corpo=email_model.corpo,
        )

        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=[
                    {
                        "codigo": "ERRO_ENVIO_EMAIL",
                        "mensagem": f"Erro ao enviar e-mail: {erro or 'Erro desconhecido'}",
                    }
                ],
            )

        # Marca como enviado após sucesso
        email_enviado = email_repo.marcar_como_enviado(novo_email.id)

        return email_enviado

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "codigo": "DADOS_INVALIDOS",
                    "mensagem": str(e),
                }
            ],
        )

