"""Servico de Equipamento - Integracao com microsservico de equipamentos"""

import os
import logging
from typing import Dict, Any, Optional, Tuple
import httpx

logger = logging.getLogger(__name__)

BASE_URL_EQUIPAMENTO = os.getenv("SERVICO_EQUIPAMENTO_URL", "http://localhost:8000")


class EquipamentoService:
    """Servico para comunicacao com o microsservico de equipamento"""

    def __init__(self, base_url: str = None, timeout: float = 10.0):
        """
        Inicializa o servico de equipamento.

        Args:
            base_url: URL base do servico de equipamento. Se None, usa a variavel de ambiente.
            timeout: Timeout para requisicoes HTTP em segundos.
        """
        self.base_url = base_url or BASE_URL_EQUIPAMENTO
        self.timeout = timeout

    def obter_bicicleta_tranca(self, id_tranca: int) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        UC03 - Passo 4: Le o numero da bicicleta presa na tranca

        Args:
            id_tranca: ID da tranca

        Returns:
            Tupla (sucesso, dados_bicicleta/erro)
        """
        try:
            logger.info(f"Verificando tranca {id_tranca} no servico-equipamento")

            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/tranca/{id_tranca}/bicicleta")

                if response.status_code == 200:
                    bicicleta = response.json()
                    logger.info(f"Bicicleta encontrada na tranca {id_tranca}: ID {bicicleta.get('id')}")
                    return True, bicicleta
                elif response.status_code == 404:
                    logger.info(f"Tranca {id_tranca} esta vazia (sem bicicleta)")
                    return True, None
                else:
                    logger.warning(f"Erro ao buscar bicicleta na tranca {id_tranca}: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao buscar bicicleta na tranca {id_tranca}")
            return False, {"error": "Timeout ao conectar com servico de equipamento"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico de equipamento")
            return False, {"error": "Erro de conexao com servico de equipamento"}
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar bicicleta na tranca {id_tranca}: {str(e)}")
            return False, {"error": str(e)}

    def destrancar(self, id_tranca: int, id_bicicleta: int) -> Tuple[bool, Dict[str, Any]]:
        """
        UC03 - Passo 10: Solicita a abertura da tranca

        Args:
            id_tranca: ID da tranca
            id_bicicleta: ID da bicicleta

        Returns:
            Tupla (sucesso, resposta/erro)
        """
        try:
            logger.info(f"Destrancando tranca {id_tranca} (bicicleta {id_bicicleta})")

            payload = {"bicicleta": id_bicicleta}

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/tranca/{id_tranca}/destrancar",
                    json=payload
                )

                if response.status_code == 200:
                    resultado = response.json()
                    logger.info(f"Tranca {id_tranca} destrancada com sucesso")
                    return True, resultado
                else:
                    logger.warning(f"Erro ao destrancar tranca {id_tranca}: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao destrancar tranca {id_tranca}")
            return False, {"error": "Timeout ao conectar com servico de equipamento"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico de equipamento")
            return False, {"error": "Erro de conexao com servico de equipamento"}
        except Exception as e:
            logger.error(f"Erro inesperado ao destrancar tranca {id_tranca}: {str(e)}")
            return False, {"error": str(e)}

    def trancar(self, id_tranca: int, id_bicicleta: int) -> Tuple[bool, Dict[str, Any]]:
        """
        UC04 - Passo 6: Solicita o fechamento da tranca

        Args:
            id_tranca: ID da tranca
            id_bicicleta: ID da bicicleta

        Returns:
            Tupla (sucesso, resposta/erro)
        """
        try:
            logger.info(f"Trancando tranca {id_tranca} (bicicleta {id_bicicleta})")

            payload = {"bicicleta": id_bicicleta}

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/tranca/{id_tranca}/trancar",
                    json=payload
                )

                if response.status_code == 200:
                    resultado = response.json()
                    logger.info(f"Tranca {id_tranca} trancada com sucesso")
                    return True, resultado
                else:
                    logger.warning(f"Erro ao trancar tranca {id_tranca}: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao trancar tranca {id_tranca}")
            return False, {"error": "Timeout ao conectar com servico de equipamento"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico de equipamento")
            return False, {"error": "Erro de conexao com servico de equipamento"}
        except Exception as e:
            logger.error(f"Erro inesperado ao trancar tranca {id_tranca}: {str(e)}")
            return False, {"error": str(e)}

    def verificar_status_bicicleta(self, id_bicicleta: int) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Verifica status da bicicleta

        Args:
            id_bicicleta: ID da bicicleta

        Returns:
            Tupla (sucesso, dados_bicicleta/erro)
        """
        try:
            logger.info(f"Verificando status da bicicleta {id_bicicleta}")

            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/bicicleta/{id_bicicleta}")

                if response.status_code == 200:
                    bicicleta = response.json()
                    logger.info(f"Bicicleta {id_bicicleta} encontrada: status {bicicleta.get('status')}")
                    return True, bicicleta
                elif response.status_code == 404:
                    logger.warning(f"Bicicleta {id_bicicleta} nao encontrada")
                    return False, {"error": "Bicicleta nao encontrada", "status_code": 404}
                else:
                    logger.warning(f"Erro ao buscar bicicleta {id_bicicleta}: status {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}

        except httpx.TimeoutException:
            logger.error(f"Timeout ao buscar bicicleta {id_bicicleta}")
            return False, {"error": "Timeout ao conectar com servico de equipamento"}
        except httpx.ConnectError:
            logger.error(f"Erro de conexao com servico de equipamento")
            return False, {"error": "Erro de conexao com servico de equipamento"}
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar bicicleta {id_bicicleta}: {str(e)}")
            return False, {"error": str(e)}


equipamento_service = EquipamentoService()
