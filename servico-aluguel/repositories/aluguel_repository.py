from typing import Optional
from tinydb import TinyDB, Query
from models.aluguel_model import Aluguel, Cobranca, StatusAluguel, StatusCobranca
from datetime import datetime

class AluguelRepository:
    def __init__(self, db: TinyDB):
        self.alugueis = db.table('alugueis')
        self.cobrancas = db.table('cobrancas')
        self.A = Query()
        self.C = Query()

    def criar_aluguel(self, ciclista: int, tranca: int, bicicleta: int, id_cobranca: int) -> Aluguel:
        """UC03: Criar novo aluguel"""
        todos = self.alugueis.all()
        proximo_id = max([a.get('id', 0) for a in todos], default=0) + 1

        dados = {
            "id": proximo_id,
            "ciclista": ciclista,
            "trancaInicio": tranca,
            "idBicicleta": bicicleta,
            "horaInicio": datetime.now().isoformat(),
            "trancaFim": None,
            "horaFim": None,
            "cobranca": id_cobranca,
            "cobrancaExtra": None,
            "status": StatusAluguel.EM_ANDAMENTO.value
        }

        self.alugueis.insert(dados)
        return Aluguel(**dados)

    def buscar_aluguel_ativo(self, id_ciclista: int) -> Optional[Aluguel]:
        """Busca aluguel em andamento do ciclista"""
        resultado = self.alugueis.get(
            (self.A.ciclista == id_ciclista) &
            (self.A.status == StatusAluguel.EM_ANDAMENTO.value)
        )
        return Aluguel(**resultado) if resultado else None

    def finalizar_aluguel(self, id_aluguel: int, tranca_fim: int, id_cobranca_extra: Optional[int]) -> Aluguel:
        """UC04: Finalizar aluguel (devolução)"""
        self.alugueis.update({
            "trancaFim": tranca_fim,
            "horaFim": datetime.now().isoformat(),
            "cobrancaExtra": id_cobranca_extra,
            "status": StatusAluguel.FINALIZADO.value
        }, self.A.id == id_aluguel)

        resultado = self.alugueis.get(self.A.id == id_aluguel)
        return Aluguel(**resultado)

    def criar_cobranca(self, valor: float, id_ciclista: int, tipo: str) -> Cobranca:
        """Criar registro de cobrança"""
        todos = self.cobrancas.all()
        proximo_id = max([c.get('id', 0) for c in todos], default=0) + 1

        dados = {
            "id": proximo_id,
            "valor": valor,
            "ciclista": id_ciclista,
            "status": StatusCobranca.PAGA.value,  # Mock: sempre paga
            "horaSolicitacao": datetime.now().isoformat(),
            "horaFinalizacao": datetime.now().isoformat(),
            "tipo": tipo
        }

        self.cobrancas.insert(dados)
        return Cobranca(**dados)
