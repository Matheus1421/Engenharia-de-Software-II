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
        """Cria uma nova cobrança"""
        # Gera um novo ID
        all_cobrancas = self.table.all()
        new_id = max([c['id'] for c in all_cobrancas], default=0) + 1
        
        cobranca_data = cobranca.model_dump(by_alias=True)
        cobranca_data['id'] = new_id
        cobranca_data['status'] = StatusCobranca.PENDENTE.value
        cobranca_data['dataCriacao'] = datetime.now(timezone.utc).isoformat()
        cobranca_data['dataPagamento'] = None
        
        self.table.insert(cobranca_data)
        return Cobranca(**cobranca_data)
    
    def get_by_id(self, cobranca_id: int) -> Optional[Cobranca]:
        """Busca uma cobrança por ID"""
        result = self.table.get(self.query.id == cobranca_id)
        if result:
            # Converte para o formato do modelo
            return Cobranca(**result)
        return None
    
    def get_all(self) -> List[Cobranca]:
        """Retorna todas as cobranças"""
        results = self.table.all()
        return [Cobranca(**r) for r in results]
    
    def update_status(self, cobranca_id: int, status: StatusCobranca, data_pagamento: Optional[str] = None) -> Optional[Cobranca]:
        """Atualiza o status de uma cobrança"""
        cobranca = self.get_by_id(cobranca_id)
        if not cobranca:
            return None
        
        update_data = {'status': status.value}
        if data_pagamento:
            update_data['dataPagamento'] = data_pagamento
        elif status == StatusCobranca.PAGA and not data_pagamento:
            update_data['dataPagamento'] = datetime.now(timezone.utc).isoformat()
        
        self.table.update(update_data, self.query.id == cobranca_id)
        return self.get_by_id(cobranca_id)

