from typing import List, Optional
from tinydb import TinyDB, Query
from models.funcionario_model import NovoFuncionario, Funcionario

class FuncionarioRepository:
    def __init__(self, db: TinyDB):
        self.table = db.table('funcionarios')
        self.F = Query()

    def criar(self, func: NovoFuncionario) -> Funcionario:
        """UC15: Cadastrar funcionário com matrícula auto-gerada (R2)"""
        todos = self.table.all()
        proximo_num = max([int(f.get('matricula', 'F0')[1:]) for f in todos], default=0) + 1
        matricula = f"F{proximo_num:03d}"

        dados = func.model_dump(exclude={'confirmacaoSenha'})
        dados['matricula'] = matricula
        self.table.insert(dados)

        return Funcionario(**dados)

    def listar(self) -> List[Funcionario]:
        return [Funcionario(**f) for f in self.table.all()]

    def buscar_por_matricula(self, matricula: str) -> Optional[Funcionario]:
        resultado = self.table.get(self.F.matricula == matricula)
        return Funcionario(**resultado) if resultado else None

    def atualizar(self, matricula: str, dados: dict) -> Optional[Funcionario]:
        self.table.update(dados, self.F.matricula == matricula)
        return self.buscar_por_matricula(matricula)

    def deletar(self, matricula: str) -> bool:
        return self.table.remove(self.F.matricula == matricula)
