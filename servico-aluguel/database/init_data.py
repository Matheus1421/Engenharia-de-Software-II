"""Dados iniciais para testes e demonstração"""

from datetime import datetime, timedelta
from tinydb import TinyDB

def init_db(db: TinyDB):
    """Inicializa o banco de dados com dados de exemplo"""
    print("Inicializando banco de dados com dados de exemplo...")

    # Funcionários
    funcionarios_table = db.table('funcionarios')
    funcionarios_iniciais = [
        {
            "matricula": "F001",
            "nome": "Admin Sistema",
            "idade": 35,
            "funcao": "ADMINISTRATIVO",
            "cpf": "12345678901",
            "email": "admin@scb.com",
            "senha": "admin123",
            "confirmacaoSenha": "admin123"
        },
        {
            "matricula": "F002",
            "nome": "Reparador",
            "idade": 28,
            "funcao": "REPARADOR",
            "cpf": "98765432100",
            "email": "reparador@scb.com",
            "senha": "reparador123",
            "confirmacaoSenha": "reparador123"
        }
    ]
    funcionarios_table.insert_multiple(funcionarios_iniciais)
    print(f"  ✓ {len(funcionarios_iniciais)} funcionários criados")

    # Ciclistas
    ciclistas_table = db.table('ciclistas')
    data_nascimento = (datetime.now() - timedelta(days=365*25)).strftime("%Y-%m-%d")

    ciclistas_iniciais = [
        {
            "id": 1,
            "nome": "Vasco da Gama",
            "nascimento": data_nascimento,
            "cpf": "11122233344",
            "passaporte": None,
            "nacionalidade": "BRASILEIRO",
            "email": "vasco@email.com",
            "senha": "senha123",
            "urlFotoDocumento": "https://exemplo.com/foto1.jpg",
            "status": "ATIVO",
            "dataConfirmacao": datetime.now().isoformat()
        },
        {
            "id": 2,
            "nome": "Felipe coutinho",
            "nascimento": data_nascimento,
            "cpf": None,
            "passaporte": {
                "numero": "US123456",
                "validade": "2030-12-31",
                "pais": "US"
            },
            "nacionalidade": "ESTRANGEIRO",
            "email": "coutinho@email.com",
            "senha": "senha456",
            "urlFotoDocumento": "https://exemplo.com/foto2.jpg",
            "status": "AGUARDANDO_CONFIRMACAO",
            "dataConfirmacao": None
        }
    ]
    ciclistas_table.insert_multiple(ciclistas_iniciais)
    print(f"  ✓ {len(ciclistas_iniciais)} ciclistas criados")

    # Cartões
    cartoes_table = db.table('cartoes')
    cartoes_iniciais = [
        {
            "id": 1,
            "idCiclista": 1,
            "nomeTitular": "Vasco da Gama",
            "numero": "4111111111111111",
            "validade": "2028-12-31",
            "cvv": "123"
        },
        {
            "id": 2,
            "idCiclista": 2,
            "nomeTitular": "Felipe coutinho",
            "numero": "5555555555554444",
            "validade": "2027-06-30",
            "cvv": "456"
        }
    ]
    cartoes_table.insert_multiple(cartoes_iniciais)
    print(f"  ✓ {len(cartoes_iniciais)} cartões criados")

    # Aluguéis
    alugueis_table = db.table('alugueis')
    aluguel_em_andamento = {
        "id": 1,
        "ciclista": 1,
        "trancaInicio": 1,
        "bicicleta": 1,
        "horaInicio": (datetime.now() - timedelta(hours=1)).isoformat(),
        "trancaFim": None,
        "horaFim": None,
        "cobranca": 1,
        "cobrancaExtra": None,
        "status": "EM_ANDAMENTO"
    }
    alugueis_table.insert(aluguel_em_andamento)
    print(f"  ✓ 1 aluguel em andamento criado")

    # Cobranças
    cobrancas_table = db.table('cobrancas')
    cobranca_inicial = {
        "id": 1,
        "valor": 10.00,
        "status": "PAGA",
        "horaSolicitacao": (datetime.now() - timedelta(hours=1)).isoformat(),
        "horaFinalizacao": (datetime.now() - timedelta(hours=1)).isoformat(),
        "tipo": "ALUGUEL_INICIAL"
    }
    cobrancas_table.insert(cobranca_inicial)
    print(f"  ✓ 1 cobrança criada")

    # Fila de cobranças
    fila_cobrancas_table = db.table('fila_cobrancas')
    print(f"  ✓ Tabela de fila de cobranças criada (vazia)")
