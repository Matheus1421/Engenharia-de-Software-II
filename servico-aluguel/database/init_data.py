"""Dados iniciais conforme especificacao do PDF de testes do Postman"""

from datetime import datetime, timedelta
from tinydb import TinyDB

def init_db(db: TinyDB):
    """Inicializa o banco de dados com dados conforme PDF de testes"""
    print("Inicializando banco de dados conforme especificacao do PDF...")

    # Limpar todas as tabelas
    for table_name in ['ciclistas', 'cartoes', 'funcionarios', 'alugueis', 'cobrancas', 'fila_cobrancas']:
        db.table(table_name).truncate()

    # CICLISTAS - 4 conforme PDF
    ciclistas_table = db.table('ciclistas')
    ciclistas_iniciais = [
        {
            "id": 1,
            "nome": "Fulano Beltrano",
            "nascimento": "2021-05-02",
            "cpf": "78804034009",
            "passaporte": None,
            "nacionalidade": "BRASILEIRO",
            "email": "user@example.com",
            "senha": "ABC123",
            "urlFotoDocumento": "https://exemplo.com/foto.jpg",
            "status": "ATIVO",
            "dataConfirmacao": datetime.now().isoformat()
        },
        {
            "id": 2,
            "nome": "Fulano Beltrano",
            "nascimento": "2021-05-02",
            "cpf": "43943488039",
            "passaporte": None,
            "nacionalidade": "BRASILEIRO",
            "email": "user2@example.com",
            "senha": "ABC123",
            "urlFotoDocumento": "https://exemplo.com/foto.jpg",
            "status": "AGUARDANDO_CONFIRMACAO",
            "dataConfirmacao": None
        },
        {
            "id": 3,
            "nome": "Fulano Beltrano",
            "nascimento": "2021-05-02",
            "cpf": "10243164084",
            "passaporte": None,
            "nacionalidade": "BRASILEIRO",
            "email": "user3@example.com",
            "senha": "ABC123",
            "urlFotoDocumento": "https://exemplo.com/foto.jpg",
            "status": "ATIVO",
            "dataConfirmacao": datetime.now().isoformat()
        },
        {
            "id": 4,
            "nome": "Fulano Beltrano",
            "nascimento": "2021-05-02",
            "cpf": "30880150017",
            "passaporte": None,
            "nacionalidade": "BRASILEIRO",
            "email": "user4@example.com",
            "senha": "ABC123",
            "urlFotoDocumento": "https://exemplo.com/foto.jpg",
            "status": "ATIVO",
            "dataConfirmacao": datetime.now().isoformat()
        }
    ]
    ciclistas_table.insert_multiple(ciclistas_iniciais)
    print(f"  + {len(ciclistas_iniciais)} ciclistas criados")

    # CARTOES - 4 conforme PDF (todos iguais)
    cartoes_table = db.table('cartoes')
    cartoes_iniciais = [
        {
            "id": 1,
            "idCiclista": 1,
            "nomeTitular": "Fulano Beltrano",
            "numero": "4012001037141112",
            "validade": "2022-12",
            "cvv": "132"
        },
        {
            "id": 2,
            "idCiclista": 2,
            "nomeTitular": "Fulano Beltrano",
            "numero": "4012001037141112",
            "validade": "2022-12",
            "cvv": "132"
        },
        {
            "id": 3,
            "idCiclista": 3,
            "nomeTitular": "Fulano Beltrano",
            "numero": "4012001037141112",
            "validade": "2022-12",
            "cvv": "132"
        },
        {
            "id": 4,
            "idCiclista": 4,
            "nomeTitular": "Fulano Beltrano",
            "numero": "4012001037141112",
            "validade": "2022-12",
            "cvv": "132"
        }
    ]
    cartoes_table.insert_multiple(cartoes_iniciais)
    print(f"  + {len(cartoes_iniciais)} cartoes criados")

    # FUNCIONARIOS - 1 conforme PDF
    funcionarios_table = db.table('funcionarios')
    funcionario = {
        "id": 1,
        "matricula": "12345",
        "nome": "Beltrano",
        "idade": 25,
        "funcao": "REPARADOR",
        "cpf": "99999999999",
        "email": "employee@example.com",
        "senha": "123",
        "confirmacaoSenha": "123"
    }
    funcionarios_table.insert(funcionario)
    print(f"  + 1 funcionario criado")

    # COBRANCAS - 3 conforme PDF
    cobrancas_table = db.table('cobrancas')
    agora = datetime.now()
    duas_horas_atras = agora - timedelta(hours=2)

    cobrancas_iniciais = [
        {
            "id": 1,
            "valor": 10.00,
            "ciclista": 3,
            "status": "PAGA",
            "horaSolicitacao": agora.isoformat(),
            "horaFinalizacao": agora.isoformat(),
            "tipo": "ALUGUEL_INICIAL"
        },
        {
            "id": 2,
            "valor": 10.00,
            "ciclista": 4,
            "status": "PAGA",
            "horaSolicitacao": duas_horas_atras.isoformat(),
            "horaFinalizacao": duas_horas_atras.isoformat(),
            "tipo": "ALUGUEL_INICIAL"
        },
        {
            "id": 3,
            "valor": 10.00,
            "ciclista": 3,
            "status": "PAGA",
            "horaSolicitacao": duas_horas_atras.isoformat(),
            "horaFinalizacao": duas_horas_atras.isoformat(),
            "tipo": "ALUGUEL_INICIAL"
        }
    ]
    cobrancas_table.insert_multiple(cobrancas_iniciais)
    print(f"  + {len(cobrancas_iniciais)} cobrancas criadas")

    # ALUGUEIS - 3 conforme PDF
    alugueis_table = db.table('alugueis')
    alugueis_iniciais = [
        {
            "id": 1,
            "ciclista": 3,
            "trancaInicio": 2,
            "bicicleta": 3,
            "horaInicio": agora.isoformat(),
            "trancaFim": None,
            "horaFim": None,
            "cobranca": 1,
            "cobrancaExtra": None,
            "status": "EM_ANDAMENTO"
        },
        {
            "id": 2,
            "ciclista": 4,
            "trancaInicio": 4,
            "bicicleta": 5,
            "horaInicio": duas_horas_atras.isoformat(),
            "trancaFim": None,
            "horaFim": None,
            "cobranca": 2,
            "cobrancaExtra": None,
            "status": "EM_ANDAMENTO"
        },
        {
            "id": 3,
            "ciclista": 3,
            "trancaInicio": 1,
            "bicicleta": 1,
            "horaInicio": duas_horas_atras.isoformat(),
            "trancaFim": 2,
            "horaFim": agora.isoformat(),
            "cobranca": 3,
            "cobrancaExtra": None,
            "status": "FINALIZADO"
        }
    ]
    alugueis_table.insert_multiple(alugueis_iniciais)
    print(f"  + {len(alugueis_iniciais)} alugueis criados")

    # Fila de cobrancas (vazia)
    fila_cobrancas_table = db.table('fila_cobrancas')
    print(f"  + Tabela de fila de cobrancas criada (vazia)")

    print("Banco de dados inicializado com sucesso!")
