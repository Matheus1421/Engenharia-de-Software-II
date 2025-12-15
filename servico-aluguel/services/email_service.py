"""Servico de Email - Integracao com microsservico externo"""

import os
import logging
from typing import Dict, Any, Tuple
import httpx

logger = logging.getLogger(__name__)

BASE_URL_EXTERNO = os.getenv("SERVICO_EXTERNO_URL", "http://localhost:8002")


class EmailService:
    """Servico para comunicacao com o microsservico externo (envio de emails)"""

    def __init__(self, base_url: str = None, timeout: float = 10.0):
        """
        Inicializa o servico de email.

        Args:
            base_url: URL base do servico externo. Se None, usa a variavel de ambiente.
            timeout: Timeout para requisicoes HTTP em segundos.
        """
        self.base_url = base_url or BASE_URL_EXTERNO
        self.timeout = timeout

    def enviar_email(
        self,
        email: str,
        assunto: str,
        mensagem: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Envia um email atraves do microsservico externo

        Args:
            email: Email do destinatario
            assunto: Assunto do email
            mensagem: Corpo do email

        Returns:
            Tupla (sucesso, resposta/erro)
        """
        try:
            logger.info(f"Enviando email para: {email}")

            payload = {
                "destinatario": email,
                "assunto": assunto,
                "corpo": mensagem
            }

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/email/enviar",
                    json=payload
                )

                if response.status_code == 200:
                    resultado = response.json()
                    logger.info(f"Email enviado com sucesso para {email}")
                    return True, resultado
                else:
                    logger.warning(f"Erro ao enviar email para {email}: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao enviar email para {email}")
            return False, {"error": "Timeout ao conectar com servico externo"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico externo")
            return False, {"error": "Erro de conexao com servico externo"}
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar email: {str(e)}")
            return False, {"error": str(e)}

    def enviar_confirmacao_cadastro(
        self,
        email: str,
        nome: str,
        id_ciclista: int
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        UC01 - Passo 9: Envio de email de confirmacao de cadastro

        Args:
            email: Email do ciclista
            nome: Nome do ciclista
            id_ciclista: ID do ciclista

        Returns:
            Tupla (sucesso, resposta/erro)
        """
        link_confirmacao = f"http://localhost:8001/ciclista/{id_ciclista}/ativar"

        mensagem = f"""
        Ola {nome}!

        Para ativar sua conta, clique no link abaixo:
        {link_confirmacao}

        Se voce nao se cadastrou, ignore este email.
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
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        UC03 - R4: Email com dados da retirada da bicicleta

        Args:
            email: Email do ciclista
            nome: Nome do ciclista
            bicicleta_id: ID da bicicleta
            tranca_id: ID da tranca
            valor: Valor cobrado
            hora: Horario do aluguel

        Returns:
            Tupla (sucesso, resposta/erro)
        """
        mensagem = f"""
        Ola {nome}!

        Seu aluguel foi realizado com sucesso!

        Detalhes do Aluguel:
        - Bicicleta: #{bicicleta_id}
        - Tranca de retirada: #{tranca_id}
        - Horario: {hora}
        - Valor cobrado: R$ {valor:.2f}

        Aproveite seu passeio!

        Lembre-se: apos 2 horas, sera cobrado R$ 5,00 a cada meia hora.
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
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        UC04 - R3: Email com dados da devolucao da bicicleta

        Args:
            email: Email do ciclista
            nome: Nome do ciclista
            bicicleta_id: ID da bicicleta
            tranca_id: ID da tranca
            tempo_minutos: Tempo total em minutos
            valor_total: Valor total cobrado
            taxa_extra: Taxa extra cobrada

        Returns:
            Tupla (sucesso, resposta/erro)
        """
        horas = tempo_minutos // 60
        minutos = tempo_minutos % 60

        mensagem = f"""
        Ola {nome}!

        Sua devolucao foi realizada com sucesso!

        Detalhes da Devolucao:
        - Bicicleta: #{bicicleta_id}
        - Tranca de devolucao: #{tranca_id}
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
            assunto="Devolucao realizada",
            mensagem=mensagem
        )


email_service = EmailService()
