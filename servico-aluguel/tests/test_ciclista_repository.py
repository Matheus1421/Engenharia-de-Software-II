"""
Testes unitários do CiclistaRepository.
Testa operações de CRUD e lógica de ativação (UC02).
"""
import pytest
from unittest.mock import MagicMock, Mock
from datetime import date, datetime
from repositories.ciclista_repository import CiclistaRepository
from models.ciclista_model import NovoCiclista, Ciclista, StatusCiclista, Nacionalidade


#   TESTES DE CRIAR

def test_criar_ciclista_gera_id_automatico_primeiro():
    """UC01 - Testa que criar() gera ID 1 quando banco está vazio"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []  # Banco vazio
    mock_table.insert = Mock()

    repo = CiclistaRepository(mock_db)

    ciclista_dados = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )

    resultado = repo.criar(ciclista_dados, senha="senha123")

    assert resultado.id == 1
    assert resultado.status == StatusCiclista.AGUARDANDO_CONFIRMACAO
    assert resultado.senha == "senha123"
    assert resultado.dataConfirmacao is None
    mock_table.insert.assert_called_once()


def test_criar_ciclista_gera_id_sequencial():
    """UC01 - Testa que criar() gera IDs sequenciais (1, 2, 3...)"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Simula 2 ciclistas já existentes
    mock_table.all.return_value = [
        {'id': 1, 'nome': 'Ciclista 1'},
        {'id': 2, 'nome': 'Ciclista 2'}
    ]
    mock_table.insert = Mock()

    repo = CiclistaRepository(mock_db)

    ciclista_dados = NovoCiclista(
        nome="Terceiro Ciclista",
        nascimento=date(1995, 5, 10),
        cpf="98765432100",
        email="terceiro@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )

    resultado = repo.criar(ciclista_dados, senha="senha456")

    assert resultado.id == 3  # Próximo ID sequencial


def test_criar_ciclista_define_status_inicial():
    """UC01 - Testa que criar() define status AGUARDANDO_CONFIRMACAO"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []
    mock_table.insert = Mock()

    repo = CiclistaRepository(mock_db)

    ciclista_dados = NovoCiclista(
        nome="Maria Santos",
        nascimento=date(1992, 3, 15),
        cpf="11122233344",
        email="maria@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )

    resultado = repo.criar(ciclista_dados, senha="senha789")

    assert resultado.status == StatusCiclista.AGUARDANDO_CONFIRMACAO


#   TESTES DE BUSCAR_POR_ID

def test_buscar_por_id_encontra():
    """Testa buscar_por_id quando ciclista existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.get.return_value = {
        'id': 1,
        'nome': 'João Silva',
        'nascimento': '1990-01-01',
        'cpf': '12345678901',
        'email': 'joao@email.com',
        'nacionalidade': 'BRASILEIRO',
        'urlFotoDocumento': 'http://exemplo.com/foto.jpg',
        'status': 'ATIVO',
        'senha': 'senha123',
        'dataConfirmacao': '2024-01-15T10:00:00Z'
    }

    repo = CiclistaRepository(mock_db)
    resultado = repo.buscar_por_id(1)

    assert resultado is not None
    assert resultado.id == 1
    assert resultado.email == 'joao@email.com'


def test_buscar_por_id_nao_encontra():
    """Testa buscar_por_id quando ciclista não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CiclistaRepository(mock_db)
    resultado = repo.buscar_por_id(999)

    assert resultado is None


#   TESTES DE BUSCAR_POR_EMAIL

def test_buscar_por_email_encontra():
    """Testa buscar_por_email quando email existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.get.return_value = {
        'id': 2,
        'nome': 'Maria Santos',
        'nascimento': '1995-05-10',
        'cpf': '98765432100',
        'email': 'maria@email.com',
        'nacionalidade': 'BRASILEIRO',
        'urlFotoDocumento': 'http://exemplo.com/foto.jpg',
        'status': 'AGUARDANDO_CONFIRMACAO',
        'senha': 'senha456',
        'dataConfirmacao': None
    }

    repo = CiclistaRepository(mock_db)
    resultado = repo.buscar_por_email("maria@email.com")

    assert resultado is not None
    assert resultado.email == "maria@email.com"
    assert resultado.id == 2


def test_buscar_por_email_nao_encontra():
    """Testa buscar_por_email quando email não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None

    repo = CiclistaRepository(mock_db)
    resultado = repo.buscar_por_email("naoexiste@email.com")

    assert resultado is None


#   TESTES DE ATIVAR (UC02)

def test_ativar_muda_status_para_ativo():
    """UC02 - Testa que ativar() muda status para ATIVO"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Antes da ativação
    ciclista_antes = {
        'id': 1,
        'nome': 'João Silva',
        'nascimento': '1990-01-01',
        'cpf': '12345678901',
        'email': 'joao@email.com',
        'nacionalidade': 'BRASILEIRO',
        'urlFotoDocumento': 'http://exemplo.com/foto.jpg',
        'status': 'AGUARDANDO_CONFIRMACAO',
        'senha': 'senha123',
        'dataConfirmacao': None
    }

    # Depois da ativação
    ciclista_depois = ciclista_antes.copy()
    ciclista_depois['status'] = 'ATIVO'
    ciclista_depois['dataConfirmacao'] = datetime.now().isoformat()

    mock_table.get.return_value = ciclista_depois
    mock_table.update = Mock()

    repo = CiclistaRepository(mock_db)
    resultado = repo.ativar(id=1)

    assert resultado is not None
    assert resultado.status == StatusCiclista.ATIVO
    assert resultado.dataConfirmacao is not None
    mock_table.update.assert_called_once()


def test_ativar_ciclista_nao_existe():
    """UC02 - Testa que ativar() retorna None quando ciclista não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CiclistaRepository(mock_db)
    resultado = repo.ativar(id=999)

    assert resultado is None


#   TESTES DE ATUALIZAR (UC06)

def test_atualizar_ciclista_sucesso():
    """UC06 - Testa que atualizar() modifica os dados"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Ciclista antes da atualização
    ciclista_antes = {
        'id': 1,
        'nome': 'João Silva',
        'nascimento': '1990-01-01',
        'cpf': '12345678901',
        'email': 'joao@email.com',
        'nacionalidade': 'BRASILEIRO',
        'urlFotoDocumento': 'http://exemplo.com/foto_antiga.jpg',
        'status': 'ATIVO',
        'senha': 'senha123',
        'dataConfirmacao': '2024-01-15T10:00:00Z'
    }

    # Ciclista depois da atualização
    ciclista_depois = ciclista_antes.copy()
    ciclista_depois['urlFotoDocumento'] = 'http://exemplo.com/foto_nova.jpg'

    mock_table.get.return_value = ciclista_depois
    mock_table.update = Mock()

    repo = CiclistaRepository(mock_db)

    dados_novos = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto_nova.jpg"
    )

    resultado = repo.atualizar(id=1, dados=dados_novos)

    assert resultado is not None
    assert resultado.urlFotoDocumento == "http://exemplo.com/foto_nova.jpg"
    mock_table.update.assert_called_once()


def test_atualizar_ciclista_nao_encontrado():
    """UC06 - Testa que atualizar() retorna None quando ciclista não existe"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CiclistaRepository(mock_db)

    dados_novos = NovoCiclista(
        nome="João Silva",
        nascimento=date(1990, 1, 1),
        cpf="12345678901",
        email="joao@email.com",
        nacionalidade=Nacionalidade.BRASILEIRO,
        urlFotoDocumento="http://exemplo.com/foto.jpg"
    )

    resultado = repo.atualizar(id=999, dados=dados_novos)

    assert resultado is None


#   TESTES DE LISTAR

def test_listar_retorna_todos():
    """Testa que listar() retorna todos os ciclistas"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    mock_table.all.return_value = [
        {
            'id': 1,
            'nome': 'João Silva',
            'nascimento': '1990-01-01',
            'cpf': '12345678901',
            'email': 'joao@email.com',
            'nacionalidade': 'BRASILEIRO',
            'urlFotoDocumento': 'http://exemplo.com/foto1.jpg',
            'status': 'ATIVO',
            'senha': 'senha123',
            'dataConfirmacao': '2024-01-15T10:00:00Z'
        },
        {
            'id': 2,
            'nome': 'Maria Santos',
            'nascimento': '1995-05-10',
            'cpf': '98765432100',
            'email': 'maria@email.com',
            'nacionalidade': 'BRASILEIRO',
            'urlFotoDocumento': 'http://exemplo.com/foto2.jpg',
            'status': 'AGUARDANDO_CONFIRMACAO',
            'senha': 'senha456',
            'dataConfirmacao': None
        }
    ]

    repo = CiclistaRepository(mock_db)
    resultado = repo.listar()

    assert len(resultado) == 2
    assert resultado[0].id == 1
    assert resultado[1].id == 2


def test_listar_retorna_lista_vazia():
    """Testa que listar() retorna [] quando não há ciclistas"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.all.return_value = []

    repo = CiclistaRepository(mock_db)
    resultado = repo.listar()

    assert resultado == []


#   TESTES DE PODE_ALUGAR (UC03)

def test_pode_alugar_ciclista_ativo_sem_aluguel():
    """UC03 - Testa que ciclista ATIVO sem aluguel pode alugar"""
    mock_db = MagicMock()
    mock_table_ciclistas = MagicMock()
    mock_table_alugueis = MagicMock()

    mock_db.table.side_effect = lambda name: (
        mock_table_ciclistas if name == 'ciclistas' else mock_table_alugueis
    )

    # Ciclista ATIVO
    mock_table_ciclistas.get.return_value = {
        'id': 1,
        'nome': 'João Silva',
        'nascimento': '1990-01-01',
        'cpf': '12345678901',
        'email': 'joao@email.com',
        'nacionalidade': 'BRASILEIRO',
        'urlFotoDocumento': 'http://exemplo.com/foto.jpg',
        'status': 'ATIVO',
        'senha': 'senha123',
        'dataConfirmacao': '2024-01-15T10:00:00Z'
    }

    # Sem aluguel ativo
    mock_table_alugueis.search.return_value = []

    repo = CiclistaRepository(mock_db)
    resultado = repo.pode_alugar(1)

    assert resultado is True


def test_nao_pode_alugar_ciclista_aguardando():
    """UC03 - Testa que ciclista AGUARDANDO_CONFIRMACAO não pode alugar"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table

    # Ciclista AGUARDANDO_CONFIRMACAO
    mock_table.get.return_value = {
        'id': 2,
        'nome': 'Maria Santos',
        'nascimento': '1995-05-10',
        'cpf': '98765432100',
        'email': 'maria@email.com',
        'nacionalidade': 'BRASILEIRO',
        'urlFotoDocumento': 'http://exemplo.com/foto.jpg',
        'status': 'AGUARDANDO_CONFIRMACAO',
        'senha': 'senha456',
        'dataConfirmacao': None
    }

    repo = CiclistaRepository(mock_db)
    resultado = repo.pode_alugar(2)

    assert resultado is False


def test_nao_pode_alugar_ciclista_nao_existe():
    """UC03 - Testa que ciclista inexistente não pode alugar"""
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = None  # Não encontrado

    repo = CiclistaRepository(mock_db)
    resultado = repo.pode_alugar(999)

    assert resultado is False
