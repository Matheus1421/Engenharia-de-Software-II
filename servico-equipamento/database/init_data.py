"""
Arquivo para inicializar o banco de dados com dados de exemplo.
Dados conforme especificação dos testes automatizados do Postman.
"""

from models.bicicleta_model import StatusBicicleta
from models.tranca_model import StatusTranca


# Constante para localização padrão
DEFAULT_LOCALIZACAO = "Rio de Janeiro"


# Dados iniciais para bicicletas conforme testes Postman
BICICLETAS_INICIAIS = [
    {
        "id": 1,
        "marca": "Caloi",
        "modelo": "Caloi",
        "ano": "2020",
        "numero": 12345,
        "status": StatusBicicleta.DISPONIVEL.value
    },
    {
        "id": 2,
        "marca": "Caloi",
        "modelo": "Caloi",
        "ano": "2020",
        "numero": 12346,
        "status": StatusBicicleta.REPARO_SOLICITADO.value
    },
    {
        "id": 3,
        "marca": "Caloi",
        "modelo": "Caloi",
        "ano": "2020",
        "numero": 12347,
        "status": StatusBicicleta.EM_USO.value
    },
    {
        "id": 4,
        "marca": "Caloi",
        "modelo": "Caloi",
        "ano": "2020",
        "numero": 12348,
        "status": StatusBicicleta.EM_REPARO.value
    },
    {
        "id": 5,
        "marca": "Caloi",
        "modelo": "Caloi",
        "ano": "2020",
        "numero": 12349,
        "status": StatusBicicleta.DISPONIVEL.value
    }
]


# Dados iniciais para trancas conforme testes Postman
TRANCAS_INICIAIS = [
    {
        "id": 1,
        "numero": 12345,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2020",
        "modelo": "Caloi",
        "status": StatusTranca.OCUPADA.value,
        "bicicleta": 1,
        "totem": 1
    },
    {
        "id": 2,
        "numero": 12346,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2020",
        "modelo": "Caloi",
        "status": StatusTranca.LIVRE.value,
        "bicicleta": None,
        "totem": 1
    },
    {
        "id": 3,
        "numero": 12347,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2020",
        "modelo": "Caloi",
        "status": StatusTranca.OCUPADA.value,
        "bicicleta": 2,
        "totem": 1
    },
    {
        "id": 4,
        "numero": 12348,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2020",
        "modelo": "Caloi",
        "status": StatusTranca.OCUPADA.value,
        "bicicleta": 5,
        "totem": 1
    },
    {
        "id": 5,
        "numero": 12349,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2020",
        "modelo": "Caloi",
        "status": StatusTranca.EM_REPARO.value,
        "bicicleta": None,
        "totem": None
    },
    {
        "id": 6,
        "numero": 12350,
        "localizacao": DEFAULT_LOCALIZACAO,
        "anoDeFabricacao": "2020",
        "modelo": "Caloi",
        "status": StatusTranca.REPARO_SOLICITADO.value,
        "bicicleta": None,
        "totem": 1
    }
]


# Dados iniciais para totems conforme testes Postman
TOTEMS_INICIAIS = [
    {
        "id": 1,
        "localizacao": DEFAULT_LOCALIZACAO,
        "descricao": "Totem principal"
    }
]


# Relacionamento entre trancas e totems (tabela associativa)
TRANCA_TOTEM_INICIAIS = [
    {"idTranca": 1, "idTotem": 1},
    {"idTranca": 2, "idTotem": 1},
    {"idTranca": 3, "idTotem": 1},
    {"idTranca": 4, "idTotem": 1},
    {"idTranca": 6, "idTotem": 1}
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
