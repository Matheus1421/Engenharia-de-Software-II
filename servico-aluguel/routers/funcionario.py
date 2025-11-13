"""ROUTER: Funcionário - UC15"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from models.funcionario_model import Funcionario, NovoFuncionario
from repositories.funcionario_repository import FuncionarioRepository
from database.database import get_db

router = APIRouter(prefix="/funcionario", tags=["Funcionário"])

@router.get("", response_model=List[Funcionario])
def listar_funcionarios():
    """UC15: Recupera funcionários cadastrados"""
    db = get_db()
    repo = FuncionarioRepository(db)
    return repo.listar()

@router.post("", response_model=Funcionario, status_code=status.HTTP_201_CREATED)
def cadastrar_funcionario(funcionario: NovoFuncionario):
    """UC15: Cadastrar funcionário"""
    db = get_db()
    repo = FuncionarioRepository(db)
    return repo.criar(funcionario)

@router.get("/{idFuncionario}", response_model=Funcionario)
def obter_funcionario(idFuncionario: str):
    """UC15: Recupera funcionário"""
    db = get_db()
    repo = FuncionarioRepository(db)

    func = repo.buscar_por_matricula(idFuncionario)
    if not func:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return func

@router.put("/{idFuncionario}", response_model=Funcionario)
def editar_funcionario(idFuncionario: str, dados: NovoFuncionario):
    """UC15: Editar funcionário"""
    db = get_db()
    repo = FuncionarioRepository(db)

    dados_update = dados.model_dump(exclude={'senha', 'confirmacaoSenha'})
    func = repo.atualizar(idFuncionario, dados_update)

    if not func:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return func

@router.delete("/{idFuncionario}", status_code=status.HTTP_204_NO_CONTENT)
def remover_funcionario(idFuncionario: str):
    """UC15: Remover funcionário"""
    db = get_db()
    repo = FuncionarioRepository(db)

    if not repo.deletar(idFuncionario):
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
