"""
Repositório para operações CRUD de E-mails no banco de dados.
"""

from typing import List, Optional
from tinydb import Query
from datetime import datetime, timezone
from database.database import Database
from models.email_model import Email, NovoEmail


class EmailRepository:
    """Repositório para gerenciar operações de e-mails no banco de dados"""
    
    def __init__(self, db: Database):
        self.db = db
        self.table = db.get_table('emails')
        self.query = Query()
    
    def create(self, email: NovoEmail) -> Email:
        """Cria um novo e-mail"""
        # Gera um novo ID
        all_emails = self.table.all()
        new_id = max([e['id'] for e in all_emails], default=0) + 1
        
        email_data = email.model_dump()
        email_data['id'] = new_id
        email_data['enviado'] = False
        email_data['data_envio'] = None
        
        self.table.insert(email_data)
        return Email(**email_data)
    
    def get_by_id(self, email_id: int) -> Optional[Email]:
        """Busca um e-mail por ID"""
        result = self.table.get(self.query.id == email_id)
        return Email(**result) if result else None
    
    def get_all(self) -> List[Email]:
        """Retorna todos os e-mails"""
        results = self.table.all()
        return [Email(**r) for r in results]
    
    def marcar_como_enviado(self, email_id: int) -> Optional[Email]:
        """Marca um e-mail como enviado"""
        email = self.get_by_id(email_id)
        if not email:
            return None
        
        data_envio = datetime.now(timezone.utc).isoformat()
        self.table.update({
            'enviado': True,
            'data_envio': data_envio
        }, self.query.id == email_id)
        
        return self.get_by_id(email_id)

