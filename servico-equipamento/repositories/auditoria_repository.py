"""Repositório para gerenciar registros de auditoria no banco de dados."""

import logging
from typing import List, Optional
from datetime import datetime
from tinydb import Query

from models.auditoria_model import RegistroAuditoria, RegistroAuditoriaCompleto, TipoAcao, TipoEquipamento

logger = logging.getLogger(__name__)


class AuditoriaRepository:
    """Repositório para operações de auditoria"""
    
    TABLE_NAME = "auditorias"
    
    def __init__(self, db):
        """
        Inicializa o repositório de auditoria.
        
        Args:
            db: Instância do banco de dados TinyDB
        """
        self.db = db
        self.table = db.get_table(self.TABLE_NAME)
    
    def create(self, registro: RegistroAuditoria) -> RegistroAuditoriaCompleto:
        """
        Cria um novo registro de auditoria.
        
        Args:
            registro: Dados do registro de auditoria
            
        Returns:
            Registro de auditoria criado com ID
        """
        # Converte para dicionário
        registro_dict = registro.model_dump()
        
        # Converte datetime para string ISO format
        if isinstance(registro_dict.get('data_hora'), datetime):
            registro_dict['data_hora'] = registro_dict['data_hora'].isoformat()
        
        # Insere no banco de dados
        registro_id = self.table.insert(registro_dict)
        
        logger.info(
            f"Registro de auditoria criado: ID={registro_id}, "
            f"Ação={registro.tipo_acao.value}, "
            f"Equipamento={registro.tipo_equipamento.value} #{registro.numero_equipamento}, "
            f"Funcionário={registro.id_funcionario}"
        )
        
        # Retorna o registro completo
        return RegistroAuditoriaCompleto(id=registro_id, **registro_dict)
    
    def get_by_id(self, registro_id: int) -> Optional[RegistroAuditoriaCompleto]:
        """
        Busca um registro de auditoria por ID.
        
        Args:
            registro_id: ID do registro
            
        Returns:
            Registro encontrado ou None
        """
        registro = self.table.get(doc_id=registro_id)
        if registro:
            return RegistroAuditoriaCompleto(id=registro_id, **registro)
        return None
    
    def get_all(self) -> List[RegistroAuditoriaCompleto]:
        """
        Retorna todos os registros de auditoria.
        
        Returns:
            Lista de todos os registros de auditoria
        """
        registros = []
        for doc in self.table.all():
            registros.append(
                RegistroAuditoriaCompleto(id=doc.doc_id, **doc)
            )
        return registros
    
    def get_by_funcionario(self, id_funcionario: int) -> List[RegistroAuditoriaCompleto]:
        """
        Busca registros de auditoria por funcionário.
        
        Args:
            id_funcionario: ID do funcionário
            
        Returns:
            Lista de registros do funcionário
        """
        Auditoria = Query()
        resultados = self.table.search(Auditoria.id_funcionario == id_funcionario)
        
        registros = []
        for doc in resultados:
            registros.append(
                RegistroAuditoriaCompleto(id=doc.doc_id, **doc)
            )
        return registros
    
    def get_by_equipamento(
        self, 
        tipo_equipamento: TipoEquipamento, 
        id_equipamento: int
    ) -> List[RegistroAuditoriaCompleto]:
        """
        Busca registros de auditoria por equipamento.
        
        Args:
            tipo_equipamento: Tipo do equipamento (BICICLETA ou TRANCA)
            id_equipamento: ID do equipamento
            
        Returns:
            Lista de registros do equipamento
        """
        Auditoria = Query()
        resultados = self.table.search(
            (Auditoria.tipo_equipamento == tipo_equipamento.value) & 
            (Auditoria.id_equipamento == id_equipamento)
        )
        
        registros = []
        for doc in resultados:
            registros.append(
                RegistroAuditoriaCompleto(id=doc.doc_id, **doc)
            )
        return registros
    
    def get_by_tipo_acao(self, tipo_acao: TipoAcao) -> List[RegistroAuditoriaCompleto]:
        """
        Busca registros de auditoria por tipo de ação.
        
        Args:
            tipo_acao: Tipo de ação (INTEGRAR_BICICLETA, RETIRAR_BICICLETA, etc)
            
        Returns:
            Lista de registros da ação
        """
        Auditoria = Query()
        resultados = self.table.search(Auditoria.tipo_acao == tipo_acao.value)
        
        registros = []
        for doc in resultados:
            registros.append(
                RegistroAuditoriaCompleto(id=doc.doc_id, **doc)
            )
        return registros
    
    def get_ultimas_acoes_equipamento(
        self,
        tipo_equipamento: TipoEquipamento,
        id_equipamento: int,
        limit: int = 10
    ) -> List[RegistroAuditoriaCompleto]:
        """
        Busca as últimas ações de um equipamento específico.
        
        Args:
            tipo_equipamento: Tipo do equipamento
            id_equipamento: ID do equipamento
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista das últimas ações do equipamento
        """
        registros = self.get_by_equipamento(tipo_equipamento, id_equipamento)
        
        # Ordena por data_hora decrescente
        registros_ordenados = sorted(
            registros,
            key=lambda x: x.data_hora if isinstance(x.data_hora, datetime) 
                         else datetime.fromisoformat(x.data_hora),
            reverse=True
        )
        
        return registros_ordenados[:limit]
    
    def get_retiradas_em_reparo_por_funcionario(
        self,
        id_funcionario: int,
        tipo_equipamento: TipoEquipamento
    ) -> List[RegistroAuditoriaCompleto]:
        """
        Busca retiradas para reparo realizadas por um funcionário específico.
        Usado para validar se o funcionário que está devolvendo é o mesmo que retirou (UC11-R3).
        
        Args:
            id_funcionario: ID do funcionário
            tipo_equipamento: Tipo do equipamento (BICICLETA ou TRANCA)
            
        Returns:
            Lista de retiradas em reparo do funcionário
        """
        Auditoria = Query()
        
        if tipo_equipamento == TipoEquipamento.BICICLETA:
            tipo_acao = TipoAcao.RETIRAR_BICICLETA
        else:
            tipo_acao = TipoAcao.RETIRAR_TRANCA
        
        resultados = self.table.search(
            (Auditoria.id_funcionario == id_funcionario) &
            (Auditoria.tipo_acao == tipo_acao.value) &
            (Auditoria.status_destino == "EM_REPARO")
        )
        
        registros = []
        for doc in resultados:
            registros.append(
                RegistroAuditoriaCompleto(id=doc.doc_id, **doc)
            )
        return registros
    
    def verificar_reparador_original(
        self,
        tipo_equipamento: TipoEquipamento,
        id_equipamento: int,
        id_funcionario: int
    ) -> bool:
        """
        Verifica se o funcionário foi quem retirou o equipamento para reparo.
        Implementa UC11-R3: verificar se funcionário que devolve é o mesmo que retirou.
        
        Args:
            tipo_equipamento: Tipo do equipamento
            id_equipamento: ID do equipamento
            id_funcionario: ID do funcionário a verificar
            
        Returns:
            True se o funcionário foi quem retirou, False caso contrário
        """
        Auditoria = Query()
        
        if tipo_equipamento == TipoEquipamento.BICICLETA:
            tipo_acao = TipoAcao.RETIRAR_BICICLETA
        else:
            tipo_acao = TipoAcao.RETIRAR_TRANCA
        
        # Busca a última retirada em reparo deste equipamento
        resultados = self.table.search(
            (Auditoria.tipo_equipamento == tipo_equipamento.value) &
            (Auditoria.id_equipamento == id_equipamento) &
            (Auditoria.tipo_acao == tipo_acao.value) &
            (Auditoria.status_destino == "EM_REPARO")
        )
        
        if not resultados:
            return True  # Não há registro de retirada, permite a operação
        
        # Filtra resultados válidos com data_hora
        resultados_validos = [r for r in resultados if r.get('data_hora')]
        
        if not resultados_validos:
            return True  # Não há registros válidos, permite a operação
        
        # Pega o registro mais recente
        ultimo_registro = sorted(
            resultados_validos,
            key=lambda x: x.get('data_hora', ''),
            reverse=True
        )[0]
        
        return ultimo_registro.get('id_funcionario') == id_funcionario
