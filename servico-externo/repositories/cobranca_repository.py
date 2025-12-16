"""
Repositório para operações CRUD de Cobranças no banco de dados.
"""

from typing import List, Optional
from tinydb import Query
from datetime import datetime, timezone
from database.database import Database
from models.cobranca_model import Cobranca, NovaCobranca, StatusCobranca


class CobrancaRepository:
    """Repositório para gerenciar operações de cobranças no banco de dados"""

    def __init__(self, db: Database):
        self.db = db
        self.table = db.get_table('cobrancas')
        self.query = Query()

    def create(self, cobranca: NovaCobranca) -> Cobranca:
        """Cria uma nova cobrança - compatível com Postman e servico-aluguel"""
        # Gera um novo ID
        all_cobrancas = self.table.all()
        new_id = max([c['id'] for c in all_cobrancas], default=0) + 1

        agora = datetime.now(timezone.utc).isoformat()

        # Usa status enviado ou PAGA como padrão (simula pagamento automático)
        status = cobranca.status if cobranca.status else StatusCobranca.PAGA.value

        # Usa horaSolicitacao enviada ou agora
        hora_solicitacao = cobranca.horaSolicitacao if cobranca.horaSolicitacao else agora

        # Usa horaFinalizacao enviada ou agora (se status é PAGA)
        hora_finalizacao = cobranca.horaFinalizacao
        if not hora_finalizacao and status == StatusCobranca.PAGA.value:
            hora_finalizacao = agora

        cobranca_data = {
            'id': new_id,
            'ciclista': cobranca.ciclista,
            'valor': cobranca.valor,
            'status': status,
            'horaSolicitacao': hora_solicitacao,
            'horaFinalizacao': hora_finalizacao
        }

        self.table.insert(cobranca_data)
        return Cobranca(**cobranca_data)
    
    def get_by_id(self, cobranca_id: int) -> Optional[Cobranca]:
        """Busca uma cobrança por ID"""
        result = self.table.get(self.query.id == cobranca_id)
        if result:
            # Garante que todos os campos necessários existem
            cobranca_data = {
                'id': result.get('id'),
                'ciclista': result.get('ciclista') or result.get('id_ciclista'),
                'valor': result.get('valor'),
                'status': result.get('status', 'PENDENTE'),
                'horaSolicitacao': result.get('horaSolicitacao') or result.get('dataCriacao') or datetime.now(timezone.utc).isoformat(),
                'horaFinalizacao': result.get('horaFinalizacao') or result.get('dataPagamento')
            }
            return Cobranca(**cobranca_data)
        return None

    def get_all(self) -> List[Cobranca]:
        """Retorna todas as cobranças"""
        results = self.table.all()
        cobrancas = []
        for r in results:
            cobranca_data = {
                'id': r.get('id'),
                'ciclista': r.get('ciclista') or r.get('id_ciclista'),
                'valor': r.get('valor'),
                'status': r.get('status', 'PENDENTE'),
                'horaSolicitacao': r.get('horaSolicitacao') or r.get('dataCriacao') or datetime.now(timezone.utc).isoformat(),
                'horaFinalizacao': r.get('horaFinalizacao') or r.get('dataPagamento')
            }
            cobrancas.append(Cobranca(**cobranca_data))
        return cobrancas

    def update_status(self, cobranca_id: int, status: StatusCobranca, hora_finalizacao: Optional[str] = None) -> Optional[Cobranca]:
        """Atualiza o status de uma cobrança"""
        cobranca = self.get_by_id(cobranca_id)
        if not cobranca:
            return None

        update_data = {'status': status.value}
        if hora_finalizacao:
            update_data['horaFinalizacao'] = hora_finalizacao
        elif status == StatusCobranca.PAGA and not hora_finalizacao:
            update_data['horaFinalizacao'] = datetime.now(timezone.utc).isoformat()

        self.table.update(update_data, self.query.id == cobranca_id)
        return self.get_by_id(cobranca_id)

