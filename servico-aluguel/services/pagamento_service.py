"""Servico de Pagamento - Integracao com microsservico externo"""

import os
import logging
from typing import Dict, Any, Tuple
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)

BASE_URL_EXTERNO = os.getenv("SERVICO_EXTERNO_URL", "http://localhost:8002")


class PagamentoService:
    """Servico para comunicacao com o microsservico externo (cobrancas e validacao de cartao)"""

    def __init__(self, base_url: str = None, timeout: float = 10.0):
        """
        Inicializa o servico de pagamento.

        Args:
            base_url: URL base do servico externo. Se None, usa a variavel de ambiente.
            timeout: Timeout para requisicoes HTTP em segundos.
        """
        self.base_url = base_url or BASE_URL_EXTERNO
        self.timeout = timeout

    def validar_cartao(
        self,
        numero: str,
        nome_titular: str,
        validade: str,
        cvv: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        UC01 - Passo 7: Validacao de cartao com Administradora CC

        Args:
            numero: Numero do cartao
            nome_titular: Nome do titular
            validade: Data de validade
            cvv: Codigo de seguranca

        Returns:
            Tupla (sucesso, dados_validacao/erro)
        """
        try:
            logger.info(f"Validando cartao terminado em {numero[-4:]}")

            payload = {
                "numero": numero,
                "nomeTitular": nome_titular,
                "validade": validade,
                "cvv": cvv
            }

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/cartao/validar",
                    json=payload
                )

                if response.status_code == 200:
                    resultado = response.json()
                    logger.info(f"Cartao validado com sucesso: {resultado.get('valido', False)}")
                    return True, resultado
                else:
                    logger.warning(f"Erro ao validar cartao: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao validar cartao")
            return False, {"error": "Timeout ao conectar com servico externo"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico externo")
            return False, {"error": "Erro de conexao com servico externo"}
        except Exception as e:
            logger.error(f"Erro inesperado ao validar cartao: {str(e)}")
            return False, {"error": str(e)}

    def cobrar(
        self,
        valor: float,
        id_ciclista: int,
        descricao: str = "Aluguel SCB"
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        UC03: Cobranca imediata

        Args:
            valor: Valor a ser cobrado
            id_ciclista: ID do ciclista
            descricao: Descricao da cobranca

        Returns:
            Tupla (sucesso, dados_cobranca/erro)
        """
        try:
            logger.info(f"Cobrando R$ {valor:.2f} do ciclista {id_ciclista}")

            payload = {
                "valor": valor,
                "ciclista": id_ciclista,
                "status": "PAGA",
                "horaSolicitacao": datetime.now().isoformat(),
                "horaFinalizacao": datetime.now().isoformat()
            }

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/cobranca",
                    json=payload
                )

                if response.status_code == 200:
                    resultado = response.json()
                    logger.info(f"Cobranca realizada com sucesso: ID {resultado.get('id')}")
                    return True, resultado
                else:
                    logger.warning(f"Erro ao realizar cobranca: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao realizar cobranca")
            return False, {"error": "Timeout ao conectar com servico externo"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico externo")
            return False, {"error": "Erro de conexao com servico externo"}
        except Exception as e:
            logger.error(f"Erro inesperado ao realizar cobranca: {str(e)}")
            return False, {"error": str(e)}

    def adicionar_fila_cobranca(
        self,
        valor: float,
        id_ciclista: int
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        UC04, UC16: Adiciona cobranca na fila

        Args:
            valor: Valor a ser cobrado
            id_ciclista: ID do ciclista

        Returns:
            Tupla (sucesso, dados_cobranca/erro)
        """
        try:
            logger.info(f"Adicionando R$ {valor:.2f} na fila de cobranca do ciclista {id_ciclista}")

            payload = {
                "valor": valor,
                "ciclista": id_ciclista,
                "status": "PENDENTE",
                "horaSolicitacao": datetime.now().isoformat()
            }

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/cobranca",
                    json=payload
                )

                if response.status_code == 200:
                    resultado = response.json()
                    logger.info(f"Cobranca adicionada a fila: ID {resultado.get('id')}")
                    return True, resultado
                else:
                    logger.warning(f"Erro ao adicionar cobranca na fila: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao adicionar cobranca na fila")
            return False, {"error": "Timeout ao conectar com servico externo"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico externo")
            return False, {"error": "Erro de conexao com servico externo"}
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar cobranca na fila: {str(e)}")
            return False, {"error": str(e)}


pagamento_service = PagamentoService()
