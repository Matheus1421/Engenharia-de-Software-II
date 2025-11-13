"""Serviço de Equipamento (Mock)"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EquipamentoService:
    """Mock do serviço de equipamento"""

    def obter_bicicleta_tranca(self, id_tranca: int) -> Optional[Dict[str, Any]]:
        """
        UC03 - Passo 4: Lê o número da bicicleta presa na tranca

        Mock: Trancas ímpares têm bicicleta, pares estão vazias
        """
        logger.info(f"🔍 [MOCK] Verificando tranca {id_tranca}...")

        if id_tranca % 2 == 0:
            logger.info(f"   Tranca {id_tranca} está vazia")
            return None

        bicicleta = {
            "id": id_tranca,
            "numero": id_tranca,
            "status": "DISPONIVEL",
            "marca": "Caloi",
            "modelo": "Urban"
        }

        logger.info(f"   Bicicleta #{bicicleta['id']} encontrada")
        return bicicleta

    def destrancar(self, id_tranca: int, id_bicicleta: int) -> Dict[str, Any]:
        """
        UC03 - Passo 10: Solicita a abertura da tranca

        Mock: Sempre sucesso
        """
        logger.info(f"🔓 [MOCK] Destrancando tranca {id_tranca} (bicicleta {id_bicicleta})")

        if id_tranca > 100:
            return {
                "status": "error",
                "message": "Tranca não encontrada"
            }

        return {
            "status": "success",
            "message": f"Tranca {id_tranca} aberta com sucesso",
            "tranca": {
                "id": id_tranca,
                "status": "LIVRE"
            }
        }

    def trancar(self, id_tranca: int, id_bicicleta: int) -> Dict[str, Any]:
        """
        UC04 - Passo 6: Solicita o fechamento da tranca

        Mock: Sempre sucesso
        """
        logger.info(f"🔒 [MOCK] Trancando tranca {id_tranca} (bicicleta {id_bicicleta})")

        if id_tranca > 100:
            return {
                "status": "error",
                "message": "Tranca não encontrada"
            }

        return {
            "status": "success",
            "message": f"Tranca {id_tranca} fechada com sucesso",
            "tranca": {
                "id": id_tranca,
                "status": "OCUPADA",
                "bicicleta": id_bicicleta
            }
        }

    def verificar_status_bicicleta(self, id_bicicleta: int) -> Dict[str, Any]:
        """
        Verifica status da bicicleta

        Mock: Bicicletas com id múltiplo de 10 estão em reparo
        """
        logger.info(f"🔍 [MOCK] Verificando status da bicicleta {id_bicicleta}")

        if id_bicicleta % 10 == 0:
            return {
                "id": id_bicicleta,
                "status": "EM_REPARO"
            }

        return {
            "id": id_bicicleta,
            "status": "DISPONIVEL"
        }

equipamento_service = EquipamentoService()
