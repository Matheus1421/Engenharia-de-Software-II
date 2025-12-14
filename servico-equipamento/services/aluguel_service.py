"""
Serviço para comunicação com o microsserviço de aluguel.
Implementa chamadas HTTP para validação de funcionários e outras operações.
"""

import os
import logging
from typing import Dict, Any, Optional, Tuple
import httpx

logger = logging.getLogger(__name__)

# URL base do serviço de aluguel (configurável via variável de ambiente)
BASE_URL_ALUGUEL = os.getenv("BASE_URL_ALUGUEL", "http://localhost:8001")


class AluguelService:
    """Serviço para comunicação com o microsserviço de aluguel"""
    
    def __init__(self, base_url: str = None, timeout: float = 10.0):
        """
        Inicializa o serviço de aluguel.
        
        Args:
            base_url: URL base do serviço de aluguel. Se None, usa a variável de ambiente.
            timeout: Timeout para requisições HTTP em segundos.
        """
        self.base_url = base_url or BASE_URL_ALUGUEL
        self.timeout = timeout
    
    def obter_funcionario(self, id_funcionario: int) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Obtém os dados de um funcionário do microsserviço de aluguel.
        
        Args:
            id_funcionario: ID do funcionário
            
        Returns:
            Tupla (sucesso, dados_funcionario/erro)
        """
        try:
            logger.info(f"🔍 Buscando funcionário {id_funcionario}...")
            
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/funcionario/{id_funcionario}")
                
                if response.status_code == 200:
                    funcionario = response.json()
                    logger.info(f"✅ Funcionário {id_funcionario} encontrado: {funcionario.get('nome', 'N/A')}")
                    return True, funcionario
                elif response.status_code == 404:
                    logger.warning(f"⚠️ Funcionário {id_funcionario} não encontrado")
                    return False, {"error": "Funcionário não encontrado", "status_code": 404}
                else:
                    logger.warning(f"⚠️ Erro ao buscar funcionário: {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}
                    
        except httpx.TimeoutException:
            logger.error(f"❌ Timeout ao buscar funcionário {id_funcionario}")
            return False, {"error": "Timeout ao conectar com serviço de aluguel"}
        except httpx.ConnectError:
            logger.error(f"❌ Erro de conexão com serviço de aluguel")
            return False, {"error": "Erro de conexão com serviço de aluguel"}
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao buscar funcionário: {str(e)}")
            return False, {"error": str(e)}
    
    def validar_funcionario(self, id_funcionario: int) -> Tuple[bool, Optional[str]]:
        """
        Valida se um funcionário existe e está ativo.
        
        Args:
            id_funcionario: ID do funcionário a validar
            
        Returns:
            Tupla (funcionario_valido, email_funcionario ou None)
        """
        sucesso, dados = self.obter_funcionario(id_funcionario)
        
        if sucesso and dados:
            # Funcionário válido, retorna email para notificações
            email = dados.get("email")
            return True, email
        
        return False, None
    
    def obter_ciclista(self, id_ciclista: int) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Obtém os dados de um ciclista do microsserviço de aluguel.
        
        Args:
            id_ciclista: ID do ciclista
            
        Returns:
            Tupla (sucesso, dados_ciclista/erro)
        """
        try:
            logger.info(f"🔍 Buscando ciclista {id_ciclista}...")
            
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/ciclista/{id_ciclista}")
                
                if response.status_code == 200:
                    ciclista = response.json()
                    logger.info(f"✅ Ciclista {id_ciclista} encontrado")
                    return True, ciclista
                elif response.status_code == 404:
                    logger.warning(f"⚠️ Ciclista {id_ciclista} não encontrado")
                    return False, {"error": "Ciclista não encontrado", "status_code": 404}
                else:
                    logger.warning(f"⚠️ Erro ao buscar ciclista: {response.status_code}")
                    return False, {"error": response.text, "status_code": response.status_code}
                    
        except httpx.TimeoutException:
            logger.error(f"❌ Timeout ao buscar ciclista {id_ciclista}")
            return False, {"error": "Timeout ao conectar com serviço de aluguel"}
        except httpx.ConnectError:
            logger.error(f"❌ Erro de conexão com serviço de aluguel")
            return False, {"error": "Erro de conexão com serviço de aluguel"}
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao buscar ciclista: {str(e)}")
            return False, {"error": str(e)}


# Instância singleton do serviço
aluguel_service = AluguelService()
