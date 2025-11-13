"""Serviço de Pagamento (Mock)"""

from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PagamentoService:
    """Mock do serviço de pagamento"""

    def validar_cartao(
        self,
        numero: str,
        nome_titular: str,
        validade: str,
        cvv: str
    ) -> Dict[str, Any]:
        """
        UC01 - Passo 7: Validação de cartão com Administradora CC

        Mock: Sempre válido (exceto cartões com número iniciando em "0000")
        """
        logger.info(f"💳 [MOCK] Validando cartão: **** **** **** {numero[-4:]}")

        if numero.startswith("0000"):
            return {
                "valido": False,
                "motivo": "Cartão recusado pela operadora"
            }

        return {
            "valido": True,
            "token": f"tok_{numero[-4:]}_mock"
        }

    def cobrar(
        self,
        valor: float,
        id_ciclista: int,
        descricao: str = "Aluguel SCB"
    ) -> Dict[str, Any]:
        """
        UC03: Cobrança imediata

        Mock: Sempre aprovado (exceto valores > 1000)
        """
        logger.info(f"💰 [MOCK] Cobrando R$ {valor:.2f} do ciclista {id_ciclista}")

        if valor > 1000:
            return {
                "id": None,
                "status": "FALHA",
                "motivo": "Limite de crédito excedido",
                "horaSolicitacao": datetime.now().isoformat()
            }

        return {
            "id": 1,
            "status": "PAGA",
            "valor": valor,
            "ciclista": id_ciclista,
            "horaSolicitacao": datetime.now().isoformat(),
            "horaFinalizacao": datetime.now().isoformat()
        }

    def adicionar_fila_cobranca(
        self,
        valor: float,
        id_ciclista: int
    ) -> Dict[str, Any]:
        """
        UC04, UC16: Adiciona cobrança na fila

        Mock: Sempre aceita na fila
        """
        logger.info(f"📋 [MOCK] Adicionando R$ {valor:.2f} na fila de cobrança do ciclista {id_ciclista}")

        return {
            "id": 1,
            "status": "PENDENTE",
            "valor": valor,
            "ciclista": id_ciclista,
            "horaSolicitacao": datetime.now().isoformat(),
            "mensagem": "Cobrança adicionada à fila (será processada em breve)"
        }

    def processar_fila_cobrancas(self) -> Dict[str, Any]:
        """
        UC16: Processa cobranças pendentes

        Mock: Simula processamento bem-sucedido
        """
        logger.info("⚙️  [MOCK] Processando fila de cobranças...")

        return {
            "processadas": 0,
            "sucesso": 0,
            "falhas": 0,
            "mensagem": "Nenhuma cobrança pendente (MOCK)"
        }

pagamento_service = PagamentoService()
