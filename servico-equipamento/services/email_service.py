"""
Serviço para comunicação com o microsserviço externo (envio de emails).
Implementa chamadas HTTP para notificações de operações com equipamentos.
"""

import os
import logging
from typing import Dict, Any, Optional, Tuple
import httpx

logger = logging.getLogger(__name__)

# URL base do serviço externo (configurável via variável de ambiente)
BASE_URL_EXTERNO = os.getenv("BASE_URL_EXTERNO", "http://localhost:8002")


class EmailService:
    """Serviço para envio de emails via microsserviço externo"""
    
    def __init__(self, base_url: str = None, timeout: float = 10.0):
        """
        Inicializa o serviço de email.
        
        Args:
            base_url: URL base do serviço externo. Se None, usa a variável de ambiente.
            timeout: Timeout para requisições HTTP em segundos.
        """
        self.base_url = base_url or BASE_URL_EXTERNO
        self.timeout = timeout
    
    def enviar_email(
        self,
        destinatario: str,
        assunto: str,
        mensagem: str
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Envia um email através do microsserviço externo.
        
        Args:
            destinatario: Endereço de email do destinatário
            assunto: Assunto do email
            mensagem: Corpo do email
            
        Returns:
            Tupla (sucesso, resposta/erro)
        """
        try:
            payload = {
                "email": destinatario,
                "assunto": assunto,
                "mensagem": mensagem
            }
            
            logger.info(f"📧 Enviando email para {destinatario}...")
            
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/enviarEmail",
                    json=payload
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ Email enviado com sucesso para {destinatario}")
                    return True, response.json()
                else:
                    logger.warning(f"⚠️ Falha ao enviar email: {response.status_code}")
                    return False, {"status_code": response.status_code, "detail": response.text}
                    
        except httpx.TimeoutException:
            logger.error(f"❌ Timeout ao enviar email para {destinatario}")
            return False, {"error": "Timeout ao conectar com serviço de email"}
        except httpx.ConnectError:
            logger.error(f"❌ Erro de conexão com serviço de email")
            return False, {"error": "Erro de conexão com serviço de email"}
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao enviar email: {str(e)}")
            return False, {"error": str(e)}
    
    def notificar_inclusao_bicicleta(
        self,
        id_bicicleta: int,
        id_tranca: int,
        id_funcionario: int,
        email_funcionario: str = None
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Envia notificação de inclusão de bicicleta na rede.
        Conforme UC - Incluir Bicicleta na Rede.
        
        Args:
            id_bicicleta: ID da bicicleta integrada
            id_tranca: ID da tranca onde foi inserida
            id_funcionario: ID do funcionário responsável
            email_funcionario: Email do funcionário (opcional)
            
        Returns:
            Tupla (sucesso, resposta/erro)
        """
        destinatario = email_funcionario or "sistema@scb.com"
        assunto = "Bicicleta integrada na rede - SCB"
        mensagem = f"""
Operação realizada com sucesso!

Detalhes da Inclusão de Bicicleta:
- Bicicleta ID: {id_bicicleta}
- Tranca ID: {id_tranca}
- Funcionário responsável: {id_funcionario}
- Status: Bicicleta DISPONÍVEL na tranca

Esta é uma notificação automática do Sistema de Controle de Bicicletário.
"""
        return self.enviar_email(destinatario, assunto, mensagem)
    
    def notificar_retirada_bicicleta(
        self,
        id_bicicleta: int,
        id_tranca: int,
        id_funcionario: int,
        status_destino: str,
        email_funcionario: str = None
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Envia notificação de retirada de bicicleta da rede.
        Conforme UC - Retirar Bicicleta da Rede.
        
        Args:
            id_bicicleta: ID da bicicleta retirada
            id_tranca: ID da tranca de onde foi retirada
            id_funcionario: ID do funcionário responsável
            status_destino: Status de destino (EM_REPARO ou APOSENTADA)
            email_funcionario: Email do funcionário (opcional)
            
        Returns:
            Tupla (sucesso, resposta/erro)
        """
        destinatario = email_funcionario or "sistema@scb.com"
        assunto = f"Bicicleta retirada da rede para {status_destino} - SCB"
        mensagem = f"""
Operação realizada com sucesso!

Detalhes da Retirada de Bicicleta:
- Bicicleta ID: {id_bicicleta}
- Tranca ID: {id_tranca}
- Funcionário responsável: {id_funcionario}
- Status de destino: {status_destino}

Esta é uma notificação automática do Sistema de Controle de Bicicletário.
"""
        return self.enviar_email(destinatario, assunto, mensagem)
    
    def notificar_inclusao_tranca(
        self,
        id_tranca: int,
        id_totem: int,
        id_funcionario: int,
        email_funcionario: str = None
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Envia notificação de inclusão de tranca na rede.
        Conforme UC - Incluir Tranca na Rede.
        
        Args:
            id_tranca: ID da tranca integrada
            id_totem: ID do totem onde foi inserida
            id_funcionario: ID do funcionário responsável
            email_funcionario: Email do funcionário (opcional)
            
        Returns:
            Tupla (sucesso, resposta/erro)
        """
        destinatario = email_funcionario or "sistema@scb.com"
        assunto = "Tranca integrada na rede - SCB"
        mensagem = f"""
Operação realizada com sucesso!

Detalhes da Inclusão de Tranca:
- Tranca ID: {id_tranca}
- Totem ID: {id_totem}
- Funcionário responsável: {id_funcionario}
- Status: Tranca LIVRE no totem

Esta é uma notificação automática do Sistema de Controle de Bicicletário.
"""
        return self.enviar_email(destinatario, assunto, mensagem)
    
    def notificar_retirada_tranca(
        self,
        id_tranca: int,
        id_totem: int,
        id_funcionario: int,
        status_destino: str,
        email_funcionario: str = None
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Envia notificação de retirada de tranca da rede.
        Conforme UC - Retirar Tranca da Rede.
        
        Args:
            id_tranca: ID da tranca retirada
            id_totem: ID do totem de onde foi retirada
            id_funcionario: ID do funcionário responsável
            status_destino: Status de destino (EM_REPARO ou APOSENTADA)
            email_funcionario: Email do funcionário (opcional)
            
        Returns:
            Tupla (sucesso, resposta/erro)
        """
        destinatario = email_funcionario or "sistema@scb.com"
        assunto = f"Tranca retirada da rede para {status_destino} - SCB"
        mensagem = f"""
Operação realizada com sucesso!

Detalhes da Retirada de Tranca:
- Tranca ID: {id_tranca}
- Totem ID: {id_totem}
- Funcionário responsável: {id_funcionario}
- Status de destino: {status_destino}

Esta é uma notificação automática do Sistema de Controle de Bicicletário.
"""
        return self.enviar_email(destinatario, assunto, mensagem)


# Instância singleton do serviço
email_service = EmailService()
