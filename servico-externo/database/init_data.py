"""
Arquivo para inicializar o banco de dados com dados de exemplo.
"""

from models.cobranca_model import StatusCobranca


# Dados iniciais para e-mails
EMAILS_INICIAIS = [
    {
        "id": 1,
        "destinatario": "usuario1@example.com",
        "assunto": "Bem-vindo ao Sistema de Bicicletário",
        "corpo": "Olá! Bem-vindo ao nosso sistema de bicicletário compartilhado.",
        "enviado": True,
        "data_envio": "2024-01-15T10:30:00Z"
    },
    {
        "id": 2,
        "destinatario": "usuario2@example.com",
        "assunto": "Cobrança Pendente",
        "corpo": "Você possui uma cobrança pendente no valor de R$ 50,00.",
        "enviado": True,
        "data_envio": "2024-01-16T14:20:00Z"
    }
]


# Dados iniciais para cobranças (formato compatível com Postman e servico-aluguel)
COBRANCAS_INICIAIS = [
    {
        "id": 1,
        "ciclista": 1,
        "valor": 50.00,
        "status": StatusCobranca.PENDENTE.value,
        "horaSolicitacao": "2024-01-15T10:00:00Z",
        "horaFinalizacao": None
    },
    {
        "id": 2,
        "ciclista": 2,
        "valor": 75.50,
        "status": StatusCobranca.PAGA.value,
        "horaSolicitacao": "2024-01-10T09:00:00Z",
        "horaFinalizacao": "2024-01-12T15:30:00Z"
    },
    {
        "id": 3,
        "ciclista": 1,
        "valor": 30.00,
        "status": StatusCobranca.VENCIDA.value,
        "horaSolicitacao": "2023-12-01T10:00:00Z",
        "horaFinalizacao": None
    }
]


# Dados iniciais para validações de cartão
VALIDACOES_CARTAO_INICIAIS = [
    {
        "id": 1,
        "numero_cartao": "4111111111111111",
        "nome_portador": "João Silva",
        "validade": "12/25",
        "cvv": "123",
        "valido": True,
        "data_validacao": "2024-01-15T11:00:00Z",
        "mensagem": "Cartão válido"
    },
    {
        "id": 2,
        "numero_cartao": "5555555555554444",
        "nome_portador": "Maria Santos",
        "validade": "06/26",
        "cvv": "456",
        "valido": True,
        "data_validacao": "2024-01-16T09:30:00Z",
        "mensagem": "Cartão válido"
    },
    {
        "id": 3,
        "numero_cartao": "1234567890123456",
        "nome_portador": "Pedro Costa",
        "validade": "01/23",
        "cvv": "789",
        "valido": False,
        "data_validacao": "2024-01-17T14:15:00Z",
        "mensagem": "Cartão expirado"
    }
]


def init_db(db_instance):
    """
    Inicializa o banco de dados com dados de exemplo.
    Remove todos os dados existentes e insere os dados iniciais.
    """
    # Trunca todas as tabelas
    db_instance.truncate_all()
    
    # Insere dados iniciais
    emails_table = db_instance.get_table('emails')
    cobrancas_table = db_instance.get_table('cobrancas')
    validacoes_table = db_instance.get_table('validacoes_cartao')
    
    # Insere e-mails
    for email in EMAILS_INICIAIS:
        emails_table.insert(email)
    
    # Insere cobranças
    for cobranca in COBRANCAS_INICIAIS:
        cobrancas_table.insert(cobranca)
    
    # Insere validações
    for validacao in VALIDACOES_CARTAO_INICIAIS:
        validacoes_table.insert(validacao)
    
    return {
        "emails": len(EMAILS_INICIAIS),
        "cobrancas": len(COBRANCAS_INICIAIS),
        "validacoes_cartao": len(VALIDACOES_CARTAO_INICIAIS)
    }

