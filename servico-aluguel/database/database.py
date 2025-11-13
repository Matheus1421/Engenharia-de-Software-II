"""Configuração do banco de dados TinyDB"""

from tinydb import TinyDB
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db.json"

_db_instance = None

def get_db() -> TinyDB:
    """Retorna instância do banco de dados (Singleton)"""
    global _db_instance

    if _db_instance is None:
        _db_instance = TinyDB(DB_PATH, indent=4, ensure_ascii=False)
        print(f"✓ Banco de dados TinyDB inicializado em: {DB_PATH}")

    return _db_instance

def close_db():
    """Fecha a conexão com o banco de dados"""
    global _db_instance

    if _db_instance is not None:
        _db_instance.close()
        _db_instance = None
        print("✓ Banco de dados fechado")

def reset_db():
    """Remove todos os dados do banco de dados"""
    db = get_db()
    db.truncate()
    print("⚠️  Banco de dados resetado (todos os dados removidos)")
