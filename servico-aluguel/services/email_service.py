"""Serviço de Email (Mock)"""

from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    """Mock do serviço de email"""

    def enviar_email(
        self,
        email: str,
        assunto: str,
        mensagem: str
    ) -> Dict[str, Any]:
        """Simula envio de email"""
        logger.info(f"📧 [MOCK] Email enviado para: {email}")
        logger.info(f"   Assunto: {assunto}")
        logger.info(f"   Mensagem: {mensagem[:100]}...")

        return {
            "status": "success",
            "id": 1,
            "message": "Email enviado com sucesso (MOCK)"
        }

    def enviar_confirmacao_cadastro(
        self,
        email: str,
        nome: str,
        id_ciclista: int
    ) -> Dict[str, Any]:
        """UC01 - Passo 9: Envio de email de confirmação de cadastro"""
        link_confirmacao = f"http://localhost:8001/ciclista/{id_ciclista}/ativar"

        mensagem = f"""
        Olá {nome}!

        Para ativar sua conta, clique no link abaixo:
        {link_confirmacao}

        Se você não se cadastrou, ignore este email.
        """

        return self.enviar_email(
            email=email,
            assunto="Confirme seu cadastro no SCB",
            mensagem=mensagem
        )

    def enviar_recibo_aluguel(
        self,
        email: str,
        nome: str,
        bicicleta_id: int,
        tranca_id: int,
        valor: float,
        hora: str
    ) -> Dict[str, Any]:
        """UC03 - R4: Email com dados da retirada da bicicleta"""
        mensagem = f"""
        Olá {nome}!

        Seu aluguel foi realizado com sucesso!

        Detalhes do Aluguel:
        - Bicicleta: #{bicicleta_id}
        - Tranca de retirada: #{tranca_id}
        - Horário: {hora}
        - Valor cobrado: R$ {valor:.2f}

        Aproveite seu passeio!

        Lembre-se: após 2 horas, será cobrado R$ 5,00 a cada meia hora.
        """

        return self.enviar_email(
            email=email,
            assunto="Aluguel realizado",
            mensagem=mensagem
        )

    def enviar_recibo_devolucao(
        self,
        email: str,
        nome: str,
        bicicleta_id: int,
        tranca_id: int,
        tempo_minutos: int,
        valor_total: float,
        taxa_extra: float
    ) -> Dict[str, Any]:
        """UC04 - R3: Email com dados da devolução da bicicleta"""
        horas = tempo_minutos // 60
        minutos = tempo_minutos % 60

        mensagem = f"""
        Olá {nome}!

        Sua devolução foi realizada com sucesso!

        Detalhes da Devolução:
        - Bicicleta: #{bicicleta_id}
        - Tranca de devolução: #{tranca_id}
        - Tempo de uso: {horas}h {minutos}min
        - Valor total: R$ {valor_total:.2f}
        """

        if taxa_extra > 0:
            mensagem += f"""
        - Taxa extra: R$ {taxa_extra:.2f} (tempo excedente)
            """

        mensagem += """

        Obrigado!

        """

        return self.enviar_email(
            email=email,
            assunto="Devolução realizada",
            mensagem=mensagem
        )

email_service = EmailService()
