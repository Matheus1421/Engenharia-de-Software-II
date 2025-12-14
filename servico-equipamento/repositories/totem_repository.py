"""
Repositório para operações CRUD de Totems no banco de dados.
"""

from typing import List, Optional
from tinydb import Query
from database.database import Database
from models.totem_model import Totem, NovoTotem


class TotemRepository:
    """Repositório para gerenciar operações de totems no banco de dados"""
    
    def __init__(self, db: Database):
        self.db = db
        self.table = db.get_table('totems')
        self.tranca_totem_table = db.get_table('tranca_totem')
        self.query = Query()
    
    def create(self, totem: NovoTotem) -> Totem:
        """Cria um novo totem"""
        # Gera um novo ID
        all_totems = self.table.all()
        new_id = max([t['id'] for t in all_totems], default=0) + 1
        
        totem_data = totem.model_dump()
        totem_data['id'] = new_id
        
        self.table.insert(totem_data)
        return Totem(**totem_data)
    
    def get_by_id(self, totem_id: int) -> Optional[Totem]:
        """Busca um totem por ID"""
        result = self.table.get(self.query.id == totem_id)
        return Totem(**result) if result else None
    
    def get_all(self) -> List[Totem]:
        """Retorna todos os totems"""
        results = self.table.all()
        return [Totem(**r) for r in results]
    
    def update(self, totem_id: int, totem: NovoTotem) -> Optional[Totem]:
        """Atualiza um totem existente"""
        if not self.table.get(self.query.id == totem_id):
            return None
        
        totem_data = totem.model_dump()
        totem_data['id'] = totem_id
        
        self.table.update(totem_data, self.query.id == totem_id)
        return Totem(**totem_data)
    
    def delete(self, totem_id: int) -> bool:
        """Remove um totem"""
        if not self.table.get(self.query.id == totem_id):
            return False
        
        # Remove também os relacionamentos com trancas
        self.tranca_totem_table.remove(self.query.idTotem == totem_id)
        
        self.table.remove(self.query.id == totem_id)
        return True
    
    def get_trancas_ids(self, totem_id: int) -> List[int]:
        """Retorna os IDs das trancas associadas ao totem"""
        tranca_ids = set()
        
        # Busca via tabela de relacionamento
        results = self.tranca_totem_table.search(self.query.idTotem == totem_id)
        for r in results:
            tranca_ids.add(r['idTranca'])
        
        # Também busca via campo direto na tabela de trancas
        trancas_table = self.db.get_table('trancas')
        trancas_diretas = trancas_table.search(self.query.totem == totem_id)
        for t in trancas_diretas:
            tranca_ids.add(t['id'])
        
        return list(tranca_ids)
