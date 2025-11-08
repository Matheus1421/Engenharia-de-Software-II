"""
Repositório para operações CRUD de Bicicletas no banco de dados.
"""

from typing import List, Optional
from tinydb import Query
from database.database import Database
from models.bicicleta_model import Bicicleta, NovaBicicleta, StatusBicicleta


class BicicletaRepository:
    """Repositório para gerenciar operações de bicicletas no banco de dados"""
    
    def __init__(self, db: Database):
        self.db = db
        self.table = db.get_table('bicicletas')
        self.query = Query()
    
    def create(self, bicicleta: NovaBicicleta) -> Bicicleta:
        """Cria uma nova bicicleta"""
        # Gera um novo ID
        all_bicicletas = self.table.all()
        new_id = max([b['id'] for b in all_bicicletas], default=0) + 1
        
        bicicleta_data = bicicleta.model_dump()
        bicicleta_data['id'] = new_id
        bicicleta_data['status'] = bicicleta_data['status'].value if hasattr(bicicleta_data['status'], 'value') else bicicleta_data['status']
        
        self.table.insert(bicicleta_data)
        return Bicicleta(**bicicleta_data)
    
    def get_by_id(self, bicicleta_id: int) -> Optional[Bicicleta]:
        """Busca uma bicicleta por ID"""
        result = self.table.get(self.query.id == bicicleta_id)
        return Bicicleta(**result) if result else None
    
    def get_all(self) -> List[Bicicleta]:
        """Retorna todas as bicicletas"""
        results = self.table.all()
        return [Bicicleta(**r) for r in results]
    
    def update(self, bicicleta_id: int, bicicleta: NovaBicicleta) -> Optional[Bicicleta]:
        """Atualiza uma bicicleta existente"""
        if not self.table.get(self.query.id == bicicleta_id):
            return None
        
        bicicleta_data = bicicleta.model_dump()
        bicicleta_data['id'] = bicicleta_id
        bicicleta_data['status'] = bicicleta_data['status'].value if hasattr(bicicleta_data['status'], 'value') else bicicleta_data['status']
        
        self.table.update(bicicleta_data, self.query.id == bicicleta_id)
        return Bicicleta(**bicicleta_data)
    
    def delete(self, bicicleta_id: int) -> bool:
        """Remove uma bicicleta"""
        if not self.table.get(self.query.id == bicicleta_id):
            return False
        
        self.table.remove(self.query.id == bicicleta_id)
        return True
    
    def update_status(self, bicicleta_id: int, status: StatusBicicleta) -> Optional[Bicicleta]:
        """Atualiza apenas o status de uma bicicleta"""
        bicicleta = self.get_by_id(bicicleta_id)
        if not bicicleta:
            return None
        
        status_value = status.value if hasattr(status, 'value') else status
        self.table.update({'status': status_value}, self.query.id == bicicleta_id)
        
        # Retorna a bicicleta atualizada
        return self.get_by_id(bicicleta_id)
