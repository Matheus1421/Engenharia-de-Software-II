"""
Testes unitários do FuncionarioRepository.
Testa operações de CRUD e geração de matrícula (UC15).
"""
import pytest
from unittest.mock import MagicMock, Mock
from repositories.funcionario_repository import FuncionarioRepository
from models.funcionario_model import NovoFuncionario, Funcionario, FuncaoFuncionario


#   TESTES DE CRIAR (UC15)

def test_criar_funcionario_gera_matricula_f001():
    """UC15 - Testa que criar() gera matrícula F001 quando banco vazio"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []  # Banco vazio
    mock_table.insert = Mock()

    repo = FuncionarioRepository(mock_db)

    funcionario_dados = NovoFuncionario(
        nome="Admin Sistema",
        idade=35,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="admin@scb.com",
        senha="admin123",
        confirmacaoSenha="admin123"
    )

    resultado = repo.criar(funcionario_dados)

    assert resultado.matricula == "F001"
    assert resultado.nome == "Admin Sistema"
    mock_table.insert.assert_called_once()


def test_criar_funcionario_gera_matricula_sequencial():
    """UC15 - Testa que criar() gera matrículas sequenciais (F001, F002, F003...)"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Simula 2 funcionários já existentes
    mock_table.all.return_value = [
        {'matricula': 'F001'},
        {'matricula': 'F002'}
    ]
    mock_table.insert = Mock()

    repo = FuncionarioRepository(mock_db)

    funcionario_dados = NovoFuncionario(
        nome="Terceiro Funcionário",
        idade=30,
        funcao=FuncaoFuncionario.REPARADOR,
        cpf="11122233344",
        email="terceiro@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )

    resultado = repo.criar(funcionario_dados)

    assert resultado.matricula == "F003"  # Sequencial


def test_criar_funcionario_matricula_formato_correto():
    """UC15 - Testa que matrícula tem formato F seguido de 3 dígitos"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []
    mock_table.insert = Mock()

    repo = FuncionarioRepository(mock_db)

    funcionario_dados = NovoFuncionario(
        nome="João Silva",
        idade=28,
        funcao=FuncaoFuncionario.REPARADOR,
        cpf="98765432100",
        email="joao@scb.com",
        senha="senha456",
        confirmacaoSenha="senha456"
    )

    resultado = repo.criar(funcionario_dados)

    assert resultado.matricula.startswith("F")
    assert len(resultado.matricula) == 4  # F + 3 dígitos
    assert resultado.matricula[1:].isdigit()  # 3 últimos são dígitos


#   TESTES DE BUSCAR_POR_MATRICULA

def test_buscar_por_matricula_encontra():
    """UC15 - Testa buscar_por_matricula quando funcionário existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.search.return_value = [{
        'matricula': 'F001',
        'nome': 'Admin Sistema',
        'idade': 35,
        'funcao': 'ADMINISTRATIVO',
        'cpf': '12345678901',
        'email': 'admin@scb.com',
        'senha': 'admin123'
    }]

    repo = FuncionarioRepository(mock_db)
    resultado = repo.buscar_por_matricula("F001")

    assert resultado is not None
    assert resultado.matricula == "F001"
    assert resultado.nome == "Admin Sistema"


def test_buscar_por_matricula_nao_encontra():
    """UC15 - Testa buscar_por_matricula quando funcionário não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.search.return_value = []  # Não encontrado

    repo = FuncionarioRepository(mock_db)
    resultado = repo.buscar_por_matricula("F999")

    assert resultado is None


#   TESTES DE ATUALIZAR (UC15)

def test_atualizar_funcionario_sucesso():
    """UC15 - Testa que atualizar() modifica os dados"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Funcionário antes
    funcionario_antes = {
        'matricula': 'F001',
        'nome': 'Admin Sistema',
        'idade': 35,
        'funcao': 'ADMINISTRATIVO',
        'cpf': '12345678901',
        'email': 'admin@scb.com',
        'senha': 'senha_antiga'
    }

    # Funcionário depois
    funcionario_depois = funcionario_antes.copy()
    funcionario_depois['senha'] = 'senha_nova'

    mock_table.search.side_effect = [[funcionario_antes], [funcionario_depois]]
    mock_table.update = Mock()

    repo = FuncionarioRepository(mock_db)

    dados_novos = NovoFuncionario(
        nome="Admin Sistema",
        idade=35,
        funcao=FuncaoFuncionario.ADMINISTRATIVO,
        cpf="12345678901",
        email="admin@scb.com",
        senha="senha_nova",
        confirmacaoSenha="senha_nova"
    )

    resultado = repo.atualizar(matricula="F001", dados=dados_novos)

    assert resultado is not None
    assert resultado.senha == "senha_nova"
    mock_table.update.assert_called_once()


def test_atualizar_funcionario_nao_encontrado():
    """UC15 - Testa que atualizar() retorna None quando funcionário não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.search.return_value = []  # Não encontrado

    repo = FuncionarioRepository(mock_db)

    dados_novos = NovoFuncionario(
        nome="João Silva",
        idade=30,
        funcao=FuncaoFuncionario.REPARADOR,
        cpf="11122233344",
        email="joao@scb.com",
        senha="senha123",
        confirmacaoSenha="senha123"
    )

    resultado = repo.atualizar(matricula="F999", dados=dados_novos)

    assert resultado is None


#   TESTES DE DELETAR (UC15)

def test_deletar_funcionario_sucesso():
    """UC15 - Testa que deletar() remove o funcionário"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Funcionário existe
    mock_table.search.return_value = [{
        'matricula': 'F003',
        'nome': 'Carlos Silva'
    }]
    mock_table.remove = Mock()

    repo = FuncionarioRepository(mock_db)
    resultado = repo.deletar(matricula="F003")

    assert resultado is True
    mock_table.remove.assert_called_once()


def test_deletar_funcionario_nao_encontrado():
    """UC15 - Testa que deletar() retorna False quando funcionário não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.search.return_value = []  # Não encontrado

    repo = FuncionarioRepository(mock_db)
    resultado = repo.deletar(matricula="F999")

    assert resultado is False


#   TESTES DE LISTAR

def test_listar_retorna_todos():
    """UC15 - Testa que listar() retorna todos os funcionários"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.all.return_value = [
        {
            'matricula': 'F001',
            'nome': 'Admin Sistema',
            'idade': 35,
            'funcao': 'ADMINISTRATIVO',
            'cpf': '12345678901',
            'email': 'admin@scb.com',
            'senha': 'admin123'
        },
        {
            'matricula': 'F002',
            'nome': 'João Reparador',
            'idade': 28,
            'funcao': 'REPARADOR',
            'cpf': '98765432100',
            'email': 'joao@scb.com',
            'senha': 'reparador123'
        }
    ]

    repo = FuncionarioRepository(mock_db)
    resultado = repo.listar()

    assert len(resultado) == 2
    assert resultado[0].matricula == "F001"
    assert resultado[1].matricula == "F002"


def test_listar_retorna_lista_vazia():
    """UC15 - Testa que listar() retorna [] quando não há funcionários"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []

    repo = FuncionarioRepository(mock_db)
    resultado = repo.listar()

    assert resultado == []
