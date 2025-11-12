"""
Repositório para operações CRUD de Validações de Cartão no banco de dados.
"""

from typing import List, Optional
from tinydb import Query
from datetime import datetime, timezone
from database.database import Database
from models.cartao_model import ValidacaoCartao, ValidarCartaoRequest


class CartaoRepository:
    """Repositório para gerenciar operações de validações de cartão no banco de dados"""
    
    def __init__(self, db: Database):
        self.db = db
        self.table = db.get_table('validacoes_cartao')
        self.query = Query()
    
    def create(self, request: ValidarCartaoRequest, valido: bool, mensagem: str) -> ValidacaoCartao:
        """Cria uma nova validação de cartão"""
        # Gera um novo ID
        all_validacoes = self.table.all()
        new_id = max([v['id'] for v in all_validacoes], default=0) + 1
        
        # Mascara o número do cartão (mostra apenas os 4 primeiros e últimos dígitos)
        numero_cartao = request.numero_cartao
        if len(numero_cartao) > 8:
            numero_mascarado = numero_cartao[:4] + "*" * (len(numero_cartao) - 8) + numero_cartao[-4:]
        else:
            numero_mascarado = "*" * len(numero_cartao)
        
        validacao_data = {
            'id': new_id,
            'numeroCartao': numero_mascarado,
            'nomePortador': request.nome_portador,
            'validade': request.validade,
            'cvv': request.cvv,
            'valido': valido,
            'dataValidacao': datetime.now(timezone.utc).isoformat(),
            'mensagem': mensagem
        }
        
        self.table.insert(validacao_data)
        return ValidacaoCartao(**validacao_data)
    
    def get_by_id(self, validacao_id: int) -> Optional[ValidacaoCartao]:
        """Busca uma validação por ID"""
        result = self.table.get(self.query.id == validacao_id)
        return ValidacaoCartao(**result) if result else None
    
    def get_all(self) -> List[ValidacaoCartao]:
        """Retorna todas as validações"""
        results = self.table.all()
        return [ValidacaoCartao(**r) for r in results]

