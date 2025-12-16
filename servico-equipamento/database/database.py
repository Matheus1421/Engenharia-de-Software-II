"""
Gerenciador do banco de dados JSON usando TinyDB.
Este módulo centraliza a conexão e inicialização do banco de dados.
"""

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from pathlib import Path
import os
import json


# Define o caminho do banco de dados
DB_DIR = Path(__file__).parent
DB_FILE = DB_DIR / "equipamentos.json"


class UTF8JSONStorage(JSONStorage):
    """Storage personalizado que força UTF-8 encoding"""
    
    def __init__(self, path, create_dirs=False, encoding='utf-8', access_mode='r+', **kwargs):
        super().__init__(path, create_dirs=create_dirs, encoding=encoding, access_mode=access_mode, **kwargs)


class Database:
    """Gerenciador singleton do banco de dados TinyDB"""
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        if self._db is None:
            # Cria o diretório se não existir
            DB_DIR.mkdir(exist_ok=True)
            
            # Inicializa o banco de dados com storage UTF-8
            self._db = TinyDB(
                DB_FILE,
                indent=4,
                ensure_ascii=False,
                storage=UTF8JSONStorage
            )
    
    @property
    def db(self) -> TinyDB:
        """Retorna a instância do banco de dados"""
        return self._db
    
    def get_table(self, name: str):
        """Retorna uma tabela específica do banco de dados"""
        return self._db.table(name)
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self._db:
            self._db.close()
    
    def truncate_all(self):
        """Remove todos os dados de todas as tabelas"""
        self._db.truncate()
        for table in ['bicicletas', 'trancas', 'totems', 'tranca_totem', 'auditorias']:
            self._db.table(table).truncate()
    
    def reset(self):
        """Reseta o banco de dados completamente"""
        self.close()
        if DB_FILE.exists():
            os.remove(DB_FILE)
        self.__init__()


# Singleton global do banco de dados
db_instance = Database()


def get_db() -> Database:
    """Retorna a instância global do banco de dados"""
    return db_instance
