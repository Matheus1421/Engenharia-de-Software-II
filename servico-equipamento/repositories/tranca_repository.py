"""
Repositório para operações CRUD de Trancas no banco de dados.
"""

from typing import List, Optional
from tinydb import Query
from database.database import Database
from models.tranca_model import Tranca, NovaTranca, StatusTranca


class TrancaRepository:
    """Repositório para gerenciar operações de trancas no banco de dados"""
    
    def __init__(self, db: Database):
        self.db = db
        self.table = db.get_table('trancas')
        self.tranca_totem_table = db.get_table('tranca_totem')
        self.query = Query()
    
    def create(self, tranca: NovaTranca) -> Tranca:
        """Cria uma nova tranca"""
        # Gera um novo ID
        all_trancas = self.table.all()
        new_id = max([t['id'] for t in all_trancas], default=0) + 1
        
        tranca_data = tranca.model_dump()
        tranca_data['id'] = new_id
        tranca_data['bicicleta'] = None
        tranca_data['status'] = tranca_data['status'].value if hasattr(tranca_data['status'], 'value') else tranca_data['status']
        
        self.table.insert(tranca_data)
        return Tranca(**tranca_data)
    
    def get_by_id(self, tranca_id: int) -> Optional[Tranca]:
        """Busca uma tranca por ID"""
        result = self.table.get(self.query.id == tranca_id)
        return Tranca(**result) if result else None
    
    def get_all(self) -> List[Tranca]:
        """Retorna todas as trancas"""
        results = self.table.all()
        return [Tranca(**r) for r in results]
    
    def update(self, tranca_id: int, tranca: NovaTranca) -> Optional[Tranca]:
        """Atualiza uma tranca existente"""
        existing = self.table.get(self.query.id == tranca_id)
        if not existing:
            return None
        
        tranca_data = tranca.model_dump()
        tranca_data['id'] = tranca_id
        tranca_data['bicicleta'] = existing.get('bicicleta')  # Mantém a bicicleta associada
        tranca_data['status'] = tranca_data['status'].value if hasattr(tranca_data['status'], 'value') else tranca_data['status']
        
        self.table.update(tranca_data, self.query.id == tranca_id)
        return Tranca(**tranca_data)
    
    def delete(self, tranca_id: int) -> bool:
        """Remove uma tranca"""
        if not self.table.get(self.query.id == tranca_id):
            return False
        
        # Remove também o relacionamento com totem
        self.tranca_totem_table.remove(self.query.idTranca == tranca_id)
        
        self.table.remove(self.query.id == tranca_id)
        return True
    
    def update_status(self, tranca_id: int, status: StatusTranca) -> Optional[Tranca]:
        """Atualiza apenas o status de uma tranca"""
        tranca = self.get_by_id(tranca_id)
        if not tranca:
            return None
        
        status_value = status.value if hasattr(status, 'value') else status
        self.table.update({'status': status_value}, self.query.id == tranca_id)
        
        return self.get_by_id(tranca_id)
    
    def associar_bicicleta(self, tranca_id: int, bicicleta_id: Optional[int]) -> Optional[Tranca]:
        """Associa ou desassocia uma bicicleta de uma tranca"""
        tranca = self.get_by_id(tranca_id)
        if not tranca:
            return None
        
        self.table.update({'bicicleta': bicicleta_id}, self.query.id == tranca_id)
        return self.get_by_id(tranca_id)
    
    def get_bicicleta_id(self, tranca_id: int) -> Optional[int]:
        """Retorna o ID da bicicleta associada à tranca"""
        tranca = self.get_by_id(tranca_id)
        return tranca.bicicleta if tranca else None
    
    def associar_totem(self, tranca_id: int, totem_id: int) -> bool:
        """Associa uma tranca a um totem"""
        # Remove associações anteriores
        self.tranca_totem_table.remove(self.query.idTranca == tranca_id)
        
        # Cria nova associação
        self.tranca_totem_table.insert({
            'idTranca': tranca_id,
            'idTotem': totem_id
        })
        return True
    
    def desassociar_totem(self, tranca_id: int) -> bool:
        """Remove a associação de uma tranca com um totem"""
        self.tranca_totem_table.remove(self.query.idTranca == tranca_id)
        return True
    
    def get_totem_id(self, tranca_id: int) -> Optional[int]:
        """Retorna o ID do totem associado à tranca"""
        result = self.tranca_totem_table.get(self.query.idTranca == tranca_id)
        return result['idTotem'] if result else None
