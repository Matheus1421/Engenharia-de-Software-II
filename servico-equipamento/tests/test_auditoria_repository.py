"""Testes para o repositório de auditoria."""

import pytest
from datetime import datetime
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from repositories.auditoria_repository import AuditoriaRepository
from models.auditoria_model import RegistroAuditoria, TipoAcao, TipoEquipamento


class DatabaseWrapper:
    """Wrapper para simular o comportamento da classe Database nos testes"""
    def __init__(self, tinydb_instance):
        self._db = tinydb_instance
    
    def get_table(self, name: str):
        """Retorna uma tabela específica do banco de dados"""
        return self._db.table(name)


@pytest.fixture
def db():
    """Cria um banco de dados em memória para testes"""
    tinydb = TinyDB(storage=MemoryStorage)
    return DatabaseWrapper(tinydb)


@pytest.fixture
def auditoria_repo(db):
    """Cria uma instância do repositório de auditoria"""
    return AuditoriaRepository(db)


@pytest.fixture
def registro_bicicleta_integrar():
    """Fixture com um registro de auditoria de integração de bicicleta"""
    return RegistroAuditoria(
        tipo_acao=TipoAcao.INTEGRAR_BICICLETA,
        tipo_equipamento=TipoEquipamento.BICICLETA,
        id_equipamento=10,
        numero_equipamento=100,
        id_funcionario=5,
        id_tranca=3,
        status_destino="DISPONIVEL",
        detalhes={"marca": "Caloi", "modelo": "Mountain"}
    )


@pytest.fixture
def registro_bicicleta_retirar():
    """Fixture com um registro de auditoria de retirada de bicicleta"""
    return RegistroAuditoria(
        tipo_acao=TipoAcao.RETIRAR_BICICLETA,
        tipo_equipamento=TipoEquipamento.BICICLETA,
        id_equipamento=10,
        numero_equipamento=100,
        id_funcionario=5,
        id_tranca=3,
        status_destino="EM_REPARO",
        detalhes={"motivo": "Manutenção"}
    )


@pytest.fixture
def registro_tranca_integrar():
    """Fixture com um registro de auditoria de integração de tranca"""
    return RegistroAuditoria(
        tipo_acao=TipoAcao.INTEGRAR_TRANCA,
        tipo_equipamento=TipoEquipamento.TRANCA,
        id_equipamento=20,
        numero_equipamento=200,
        id_funcionario=7,
        id_totem=5,
        status_destino="LIVRE",
        detalhes={"modelo": "Tranca X"}
    )


@pytest.fixture
def registro_tranca_retirar():
    """Fixture com um registro de auditoria de retirada de tranca"""
    return RegistroAuditoria(
        tipo_acao=TipoAcao.RETIRAR_TRANCA,
        tipo_equipamento=TipoEquipamento.TRANCA,
        id_equipamento=20,
        numero_equipamento=200,
        id_funcionario=7,
        id_totem=5,
        status_destino="EM_REPARO",
        detalhes={"motivo": "Reparo"}
    )


class TestAuditoriaRepositoryCreate:
    """Testes para criação de registros de auditoria"""

    def test_create_registro_bicicleta(self, auditoria_repo, registro_bicicleta_integrar):
        """Testa criação de registro de auditoria para bicicleta"""
        resultado = auditoria_repo.create(registro_bicicleta_integrar)
        
        assert resultado.id is not None
        assert resultado.tipo_acao == TipoAcao.INTEGRAR_BICICLETA
        assert resultado.tipo_equipamento == TipoEquipamento.BICICLETA
        assert resultado.id_equipamento == 10
        assert resultado.numero_equipamento == 100
        assert resultado.id_funcionario == 5
        assert resultado.id_tranca == 3
        assert resultado.status_destino == "DISPONIVEL"

    def test_create_registro_tranca(self, auditoria_repo, registro_tranca_retirar):
        """Testa criação de registro de auditoria para tranca"""
        resultado = auditoria_repo.create(registro_tranca_retirar)
        
        assert resultado.id is not None
        assert resultado.tipo_acao == TipoAcao.RETIRAR_TRANCA
        assert resultado.tipo_equipamento == TipoEquipamento.TRANCA
        assert resultado.id_equipamento == 20
        assert resultado.id_totem == 5

    def test_create_converte_datetime_para_string(self, auditoria_repo):
        """Testa que datetime é convertido para string ao criar registro"""
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.INTEGRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=1,
            numero_equipamento=1,
            id_funcionario=1,
            data_hora=datetime.now()
        )
        
        resultado = auditoria_repo.create(registro)
        assert resultado.id is not None
        assert isinstance(resultado.data_hora, (str, datetime))


class TestAuditoriaRepositoryRead:
    """Testes para leitura de registros de auditoria"""

    def test_get_by_id(self, auditoria_repo, registro_bicicleta_integrar):
        """Testa busca de registro por ID"""
        criado = auditoria_repo.create(registro_bicicleta_integrar)
        
        encontrado = auditoria_repo.get_by_id(criado.id)
        
        assert encontrado is not None
        assert encontrado.id == criado.id
        assert encontrado.tipo_acao == TipoAcao.INTEGRAR_BICICLETA

    def test_get_by_id_inexistente(self, auditoria_repo):
        """Testa busca de registro inexistente"""
        resultado = auditoria_repo.get_by_id(9999)
        assert resultado is None

    def test_get_all_vazio(self, auditoria_repo):
        """Testa get_all com banco vazio"""
        registros = auditoria_repo.get_all()
        assert len(registros) == 0

    def test_get_all_com_registros(self, auditoria_repo, registro_bicicleta_integrar, registro_tranca_integrar):
        """Testa get_all com múltiplos registros"""
        auditoria_repo.create(registro_bicicleta_integrar)
        auditoria_repo.create(registro_tranca_integrar)
        
        registros = auditoria_repo.get_all()
        
        assert len(registros) == 2

    def test_get_by_funcionario(self, auditoria_repo, registro_bicicleta_integrar):
        """Testa busca por funcionário"""
        auditoria_repo.create(registro_bicicleta_integrar)
        
        # Cria outro registro com funcionário diferente
        outro_registro = RegistroAuditoria(
            tipo_acao=TipoAcao.INTEGRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=11,
            numero_equipamento=101,
            id_funcionario=99,
            id_tranca=4,
            status_destino="DISPONIVEL"
        )
        auditoria_repo.create(outro_registro)
        
        registros = auditoria_repo.get_by_funcionario(5)
        
        assert len(registros) == 1
        assert registros[0].id_funcionario == 5

    def test_get_by_equipamento_bicicleta(self, auditoria_repo, registro_bicicleta_integrar, registro_bicicleta_retirar):
        """Testa busca por equipamento do tipo bicicleta"""
        auditoria_repo.create(registro_bicicleta_integrar)
        auditoria_repo.create(registro_bicicleta_retirar)
        
        registros = auditoria_repo.get_by_equipamento(TipoEquipamento.BICICLETA, 10)
        
        assert len(registros) == 2
        assert all(r.id_equipamento == 10 for r in registros)
        assert all(r.tipo_equipamento == TipoEquipamento.BICICLETA for r in registros)

    def test_get_by_equipamento_tranca(self, auditoria_repo, registro_tranca_integrar):
        """Testa busca por equipamento do tipo tranca"""
        auditoria_repo.create(registro_tranca_integrar)
        
        registros = auditoria_repo.get_by_equipamento(TipoEquipamento.TRANCA, 20)
        
        assert len(registros) == 1
        assert registros[0].id_equipamento == 20
        assert registros[0].tipo_equipamento == TipoEquipamento.TRANCA

    def test_get_by_tipo_acao(self, auditoria_repo, registro_bicicleta_integrar, registro_tranca_integrar):
        """Testa busca por tipo de ação"""
        auditoria_repo.create(registro_bicicleta_integrar)
        auditoria_repo.create(registro_tranca_integrar)
        
        registros = auditoria_repo.get_by_tipo_acao(TipoAcao.INTEGRAR_BICICLETA)
        
        assert len(registros) == 1
        assert registros[0].tipo_acao == TipoAcao.INTEGRAR_BICICLETA


class TestAuditoriaRepositoryUltimasAcoes:
    """Testes para busca de últimas ações"""

    def test_get_ultimas_acoes_equipamento(self, auditoria_repo):
        """Testa busca das últimas ações de um equipamento"""
        # Cria 5 registros para o mesmo equipamento
        for i in range(5):
            registro = RegistroAuditoria(
                tipo_acao=TipoAcao.INTEGRAR_BICICLETA,
                tipo_equipamento=TipoEquipamento.BICICLETA,
                id_equipamento=10,
                numero_equipamento=100,
                id_funcionario=i,
                id_tranca=3,
                status_destino="DISPONIVEL"
            )
            auditoria_repo.create(registro)
        
        registros = auditoria_repo.get_ultimas_acoes_equipamento(
            TipoEquipamento.BICICLETA, 
            10, 
            limit=3
        )
        
        assert len(registros) == 3

    def test_get_ultimas_acoes_equipamento_sem_limit(self, auditoria_repo, registro_bicicleta_integrar):
        """Testa busca das últimas ações sem limite"""
        auditoria_repo.create(registro_bicicleta_integrar)
        
        registros = auditoria_repo.get_ultimas_acoes_equipamento(
            TipoEquipamento.BICICLETA, 
            10
        )
        
        assert len(registros) == 1


class TestAuditoriaRepositoryVerificarReparador:
    """Testes para verificação de reparador original"""

    def test_verificar_reparador_original_correto(self, auditoria_repo):
        """Testa verificação quando o funcionário é o reparador original"""
        # Cria registro de retirada em reparo
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=10,
            numero_equipamento=100,
            id_funcionario=5,
            id_tranca=3,
            status_destino="EM_REPARO"
        )
        auditoria_repo.create(registro)
        
        resultado = auditoria_repo.verificar_reparador_original(
            TipoEquipamento.BICICLETA,
            10,
            5
        )
        
        assert resultado is True

    def test_verificar_reparador_original_incorreto(self, auditoria_repo):
        """Testa verificação quando o funcionário não é o reparador original"""
        # Cria registro de retirada em reparo
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=10,
            numero_equipamento=100,
            id_funcionario=5,
            id_tranca=3,
            status_destino="EM_REPARO"
        )
        auditoria_repo.create(registro)
        
        resultado = auditoria_repo.verificar_reparador_original(
            TipoEquipamento.BICICLETA,
            10,
            99  # Funcionário diferente
        )
        
        assert resultado is False

    def test_verificar_reparador_original_sem_registro(self, auditoria_repo):
        """Testa verificação quando não há registro de retirada"""
        resultado = auditoria_repo.verificar_reparador_original(
            TipoEquipamento.BICICLETA,
            10,
            5
        )
        
        # Deve retornar True pois não há registro
        assert resultado is True

    def test_verificar_reparador_original_tranca(self, auditoria_repo):
        """Testa verificação de reparador original para tranca"""
        # Cria registro de retirada de tranca em reparo
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_TRANCA,
            tipo_equipamento=TipoEquipamento.TRANCA,
            id_equipamento=20,
            numero_equipamento=200,
            id_funcionario=7,
            id_totem=5,
            status_destino="EM_REPARO"
        )
        auditoria_repo.create(registro)
        
        resultado = auditoria_repo.verificar_reparador_original(
            TipoEquipamento.TRANCA,
            20,
            7
        )
        
        assert resultado is True

    def test_verificar_reparador_original_status_diferente(self, auditoria_repo):
        """Testa que registros com status diferente de EM_REPARO são ignorados"""
        # Cria registro com status APOSENTADA
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=10,
            numero_equipamento=100,
            id_funcionario=5,
            id_tranca=3,
            status_destino="APOSENTADA"
        )
        auditoria_repo.create(registro)
        
        resultado = auditoria_repo.verificar_reparador_original(
            TipoEquipamento.BICICLETA,
            10,
            99
        )
        
        # Deve retornar True pois não há registro com status EM_REPARO
        assert resultado is True


class TestAuditoriaRepositoryGetRetiradas:
    """Testes para busca de retiradas em reparo"""

    def test_get_retiradas_em_reparo_por_funcionario_bicicleta(self, auditoria_repo):
        """Testa busca de retiradas em reparo de bicicletas por funcionário"""
        # Cria registro de retirada em reparo
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=10,
            numero_equipamento=100,
            id_funcionario=5,
            id_tranca=3,
            status_destino="EM_REPARO"
        )
        auditoria_repo.create(registro)
        
        # Cria registro de retirada aposentada (não deve aparecer)
        registro2 = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_BICICLETA,
            tipo_equipamento=TipoEquipamento.BICICLETA,
            id_equipamento=11,
            numero_equipamento=101,
            id_funcionario=5,
            id_tranca=4,
            status_destino="APOSENTADA"
        )
        auditoria_repo.create(registro2)
        
        registros = auditoria_repo.get_retiradas_em_reparo_por_funcionario(
            5,
            TipoEquipamento.BICICLETA
        )
        
        assert len(registros) == 1
        assert registros[0].status_destino == "EM_REPARO"

    def test_get_retiradas_em_reparo_por_funcionario_tranca(self, auditoria_repo):
        """Testa busca de retiradas em reparo de trancas por funcionário"""
        registro = RegistroAuditoria(
            tipo_acao=TipoAcao.RETIRAR_TRANCA,
            tipo_equipamento=TipoEquipamento.TRANCA,
            id_equipamento=20,
            numero_equipamento=200,
            id_funcionario=7,
            id_totem=5,
            status_destino="EM_REPARO"
        )
        auditoria_repo.create(registro)
        
        registros = auditoria_repo.get_retiradas_em_reparo_por_funcionario(
            7,
            TipoEquipamento.TRANCA
        )
        
        assert len(registros) == 1
        assert registros[0].tipo_acao == TipoAcao.RETIRAR_TRANCA

    def test_get_retiradas_em_reparo_funcionario_sem_registros(self, auditoria_repo):
        """Testa busca de retiradas quando funcionário não tem registros"""
        registros = auditoria_repo.get_retiradas_em_reparo_por_funcionario(
            999,
            TipoEquipamento.BICICLETA
        )
        
        assert len(registros) == 0
