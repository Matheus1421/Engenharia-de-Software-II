"""
Serviço para envio de e-mails via SMTP.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Tuple
from datetime import datetime, timezone


class EmailService:
    """Serviço para envio de e-mails via SMTP"""
    
    def __init__(self):
        # Configurações SMTP via variáveis de ambiente
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL", self.smtp_username)
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        
        # Se não houver credenciais configuradas, usa modo de simulação
        self.simulacao = not (self.smtp_username and self.smtp_password)
        
        if self.simulacao:
            print("⚠️  Modo de simulação ativado: credenciais SMTP não configuradas")
            print("   Configure as variáveis de ambiente: SMTP_USERNAME, SMTP_PASSWORD")
    
    def enviar_email(
        self,
        destinatario: str,
        assunto: str,
        corpo: str,
        corpo_html: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Envia um e-mail via SMTP.
        
        Args:
            destinatario: E-mail do destinatário
            assunto: Assunto do e-mail
            corpo: Corpo do e-mail em texto plano
            corpo_html: Corpo do e-mail em HTML (opcional)
            
        Returns:
            Tupla (sucesso, mensagem_erro)
        """
        # Se estiver em modo de simulação, apenas retorna sucesso
        if self.simulacao:
            print(f"📧 [SIMULAÇÃO] E-mail para {destinatario}: {assunto}")
            return True, None
        
        try:
            # Cria a mensagem
            if corpo_html:
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(corpo, 'plain'))
                msg.attach(MIMEText(corpo_html, 'html'))
            else:
                msg = MIMEText(corpo, 'plain')
            
            msg['Subject'] = assunto
            msg['From'] = self.smtp_from_email
            msg['To'] = destinatario
            
            # Conecta ao servidor SMTP e envia
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_use_tls:
                    server.starttls()
                
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✓ E-mail enviado com sucesso para {destinatario}")
            return True, None
            
        except smtplib.SMTPAuthenticationError as e:
            erro_msg = f"Erro de autenticação SMTP: {str(e)}"
            print(f"✗ {erro_msg}")
            return False, erro_msg
            
        except smtplib.SMTPRecipientsRefused as e:
            erro_msg = f"Destinatário recusado: {str(e)}"
            print(f"✗ {erro_msg}")
            return False, erro_msg
            
        except smtplib.SMTPServerDisconnected as e:
            erro_msg = f"Servidor SMTP desconectado: {str(e)}"
            print(f"✗ {erro_msg}")
            return False, erro_msg
            
        except Exception as e:
            erro_msg = f"Erro ao enviar e-mail: {str(e)}"
            print(f"✗ {erro_msg}")
            return False, erro_msg


# Instância global do serviço de e-mail
email_service = EmailService()

