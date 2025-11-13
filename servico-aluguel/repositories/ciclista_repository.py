from typing import List, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document
from models.ciclista_model import NovoCiclista, Ciclista, StatusCiclista
from datetime import datetime

class CiclistaRepository:
    """Repository para operações de Ciclista no banco."""

    def __init__(self, db: TinyDB):
        self.table = db.table('ciclistas')
        self.Ciclista = Query()

    def criar(self, ciclista: NovoCiclista, senha: str) -> Ciclista:
        """
        UC01 - Passo 8: Registra dados do indivíduo.

        Gera ID automático e define status inicial.
        """
        # Gera próximo ID
        todos = self.table.all()
        proximo_id = max([c.get('id', 0) for c in todos], default=0) + 1

        # Converte modelo para dict
        dados = ciclista.model_dump()
        dados['id'] = proximo_id
        dados['status'] = StatusCiclista.AGUARDANDO_CONFIRMACAO.value
        dados['senha'] = senha  # TODO: hash em produção
        dados['dataConfirmacao'] = None

        self.table.insert(dados)

        return Ciclista(**dados)

    def buscar_por_id(self, id: int) -> Optional[Ciclista]:
        """Busca ciclista por ID."""
        resultado = self.table.get(self.Ciclista.id == id)
        return Ciclista(**resultado) if resultado else None

    def buscar_por_email(self, email: str) -> Optional[Ciclista]:
        """UC01 - A1: Verifica se email já existe."""
        resultado = self.table.get(self.Ciclista.email == email)
        return Ciclista(**resultado) if resultado else None

    def atualizar(self, id: int, dados: dict) -> Optional[Ciclista]:
        """UC06: Atualizar dados do ciclista."""
        self.table.update(dados, self.Ciclista.id == id)
        return self.buscar_por_id(id)

    def ativar(self, id: int) -> Optional[Ciclista]:
        """
        UC02 - Passo 2: Ativa ciclista após confirmação de email.
        """
        self.table.update({
            'status': StatusCiclista.ATIVO.value,
            'dataConfirmacao': datetime.now().isoformat()
        }, self.Ciclista.id == id)

        return self.buscar_por_id(id)

    def pode_alugar(self, id: int) -> bool:
        """
        Verifica se ciclista pode alugar (UC03 - R1).

        Regras:
        - Status deve ser ATIVO
        - Não pode ter aluguel em andamento
        """
        ciclista = self.buscar_por_id(id)
        if not ciclista or ciclista.status != StatusCiclista.ATIVO:
            return False

        return True

    def listar(self) -> List[Ciclista]:
        """Lista todos os ciclistas"""
        return [Ciclista(**c) for c in self.table.all()]

_ciclista_repository = None

def get_ciclista_repository(db: TinyDB) -> CiclistaRepository:
    global _ciclista_repository
    if _ciclista_repository is None:
        _ciclista_repository = CiclistaRepository(db)
    return _ciclista_repository
