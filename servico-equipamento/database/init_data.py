"""
Arquivo para inicializar o banco de dados com dados de exemplo.
"""

from models.bicicleta_model import StatusBicicleta
from models.tranca_model import StatusTranca


# Constante para localização padrão
DEFAULT_LOCALIZACAO = "-22.9068, -43.1729"


# Dados iniciais para bicicletas
BICICLETAS_INICIAIS = [
    {
        "id": 1,
        "marca": "Caloi",
        "modelo": "Mountain Bike Pro",
        "ano": "2023",
        "numero": 100,
        "status": StatusBicicleta.DISPONIVEL.value
    },
    {
        "id": 2,
        "marca": "Shimano",
        "modelo": "City Bike",
        "ano": "2023",
        "numero": 101,
        "status": StatusBicicleta.DISPONIVEL.value
    },
    {
        "id": 3,
        "marca": "Trek",
        "modelo": "Speed Master",
        "ano": "2024",
        "numero": 102,
        "status": StatusBicicleta.NOVA.value
    }
]


# Dados iniciais para trancas
TRANCAS_INICIAIS = [
    {
        "id": 1,
        "numero": 1,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2023",
        "modelo": "Tranca Smart v1",
        "status": StatusTranca.LIVRE.value,
        "bicicleta": None
    },
    {
        "id": 2,
        "numero": 2,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2023",
        "modelo": "Tranca Smart v1",
        "status": StatusTranca.LIVRE.value,
        "bicicleta": None
    },
    {
        "id": 3,
        "numero": 3,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2024",
        "modelo": "Tranca Smart v2",
        "status": StatusTranca.NOVA.value,
        "bicicleta": None
    }
]


# Dados iniciais para totems
TOTEMS_INICIAIS = [
    {
        "id": 1,
        "localizacao": DEFAULT_LOCALIZACAO,
        "descricao": "Totem da Praça Central - Centro"
    },
    {
        "id": 2,
        "localizacao": "-22.9110, -43.1780",
        "descricao": "Totem do Parque Municipal"
    }
]


# Relacionamento entre trancas e totems (tabela associativa)
TRANCA_TOTEM_INICIAIS = [
    {"idTranca": 1, "idTotem": 1},
    {"idTranca": 2, "idTotem": 1},
    {"idTranca": 3, "idTotem": 2}
]


def init_db(db_instance):
    """
    Inicializa o banco de dados com dados de exemplo.
    Remove todos os dados existentes e insere os dados iniciais.
    """
    # Trunca todas as tabelas
    db_instance.truncate_all()
    
    # Insere dados iniciais
    bicicletas_table = db_instance.get_table('bicicletas')
    trancas_table = db_instance.get_table('trancas')
    totems_table = db_instance.get_table('totems')
    tranca_totem_table = db_instance.get_table('tranca_totem')
    
    # Insere bicicletas
    for bicicleta in BICICLETAS_INICIAIS:
        bicicletas_table.insert(bicicleta)
    
    # Insere trancas
    for tranca in TRANCAS_INICIAIS:
        trancas_table.insert(tranca)
    
    # Insere totems
    for totem in TOTEMS_INICIAIS:
        totems_table.insert(totem)
    
    # Insere relacionamentos
    for rel in TRANCA_TOTEM_INICIAIS:
        tranca_totem_table.insert(rel)
    
    return {
        "bicicletas": len(BICICLETAS_INICIAIS),
        "trancas": len(TRANCAS_INICIAIS),
        "totems": len(TOTEMS_INICIAIS),
        "relacionamentos": len(TRANCA_TOTEM_INICIAIS)
    }
