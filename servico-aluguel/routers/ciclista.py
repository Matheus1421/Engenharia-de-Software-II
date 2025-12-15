"""ROUTER: Ciclista - UC01, UC02, UC06"""

from fastapi import APIRouter, HTTPException, status
from models.ciclista_model import Ciclista, CiclistaCadastro, NovoCiclista
from models.cartao_model import NovoCartaoDeCredito, CartaoDeCredito
from models.erro_model import Erro, CodigosErro
from repositories.ciclista_repository import CiclistaRepository
from repositories.cartao_repository import CartaoRepository
from repositories.aluguel_repository import AluguelRepository
from services.email_service import email_service
from services.pagamento_service import pagamento_service
from database.database import get_db

router = APIRouter(prefix="", tags=["Ciclista"])

@router.post("/ciclista", response_model=Ciclista, status_code=status.HTTP_201_CREATED)
def cadastrar_ciclista(dados: CiclistaCadastro, meio_pagamento: NovoCartaoDeCredito):
    """
    UC01: Cadastrar Ciclista

    Status 201: Criado com sucesso
    Status 422: Dados inválidos ou email já existe
    """
    db = get_db()
    ciclista_repo = CiclistaRepository(db)
    cartao_repo = CartaoRepository(db)

    # UC01 - A1: Verificar se email já existe
    if ciclista_repo.buscar_por_email(dados.ciclista.email):
        raise HTTPException(
            status_code=422,
            detail=Erro(
                codigo=CodigosErro.EMAIL_JA_CADASTRADO,
                mensagem=f"O email {dados.ciclista.email} já está cadastrado"
            ).model_dump()
        )

    # UC01 - Passo 7: Validar cartão
    sucesso_validacao, validacao = pagamento_service.validar_cartao(
        meio_pagamento.numero,
        meio_pagamento.nomeTitular,
        meio_pagamento.validade,
        meio_pagamento.cvv
    )

    if not sucesso_validacao or not validacao.get("valido"):
        raise HTTPException(
            status_code=422,
            detail=Erro(
                codigo=CodigosErro.CARTAO_INVALIDO,
                mensagem="Cartão de crédito foi recusado"
            ).model_dump()
        )

    # UC01 - Passo 8: Registrar ciclista
    ciclista = ciclista_repo.criar(dados.ciclista, dados.senha)

    # Registrar cartão
    cartao_repo.criar(ciclista.id, meio_pagamento)

    # UC01 - Passo 9: Enviar email confirmação
    sucesso_email, _ = email_service.enviar_confirmacao_cadastro(
        ciclista.email,
        ciclista.nome,
        ciclista.id
    )
    if not sucesso_email:
        print(f"Aviso: Falha ao enviar email de confirmacao para {ciclista.email}")

    return ciclista

@router.post("/ciclista/{idCiclista}/ativar", response_model=Ciclista)
def ativar_ciclista(idCiclista: int):
    """UC02: Confirmar Email / Ativar Ciclista"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)

    ciclista = ciclista_repo.buscar_por_id(idCiclista)

    if not ciclista:
        raise HTTPException(status_code=404, detail="Ciclista não encontrado")

    return ciclista_repo.ativar(idCiclista)

@router.get("/ciclista/{idCiclista}", response_model=Ciclista)
def obter_ciclista(idCiclista: int):
    """Recupera dados de um ciclista"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)

    ciclista = ciclista_repo.buscar_por_id(idCiclista)

    if not ciclista:
        raise HTTPException(status_code=404, detail="Ciclista não encontrado")

    return ciclista

@router.put("/ciclista/{idCiclista}", response_model=Ciclista)
def alterar_ciclista(idCiclista: int, dados: NovoCiclista):
    """UC06: Alterar Dados do Ciclista"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)

    if not ciclista_repo.buscar_por_id(idCiclista):
        raise HTTPException(status_code=404, detail="Ciclista não encontrado")

    dados_update = dados.model_dump(exclude_none=True)
    return ciclista_repo.atualizar(idCiclista, dados_update)

@router.get("/ciclista/{idCiclista}/permiteAluguel", response_model=bool)
def permite_aluguel(idCiclista: int):
    """Verifica se ciclista pode alugar (UC03 - R1)"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)
    aluguel_repo = AluguelRepository(db)

    if not ciclista_repo.buscar_por_id(idCiclista):
        raise HTTPException(status_code=404, detail="Ciclista não encontrado")

    pode = ciclista_repo.pode_alugar(idCiclista)
    aluguel_ativo = aluguel_repo.buscar_aluguel_ativo(idCiclista)

    return pode and (aluguel_ativo is None)

@router.get("/ciclista/{idCiclista}/bicicletaAlugada")
def bicicleta_alugada(idCiclista: int):
    """Retorna bicicleta alugada ou vazio"""
    db = get_db()
    aluguel_repo = AluguelRepository(db)

    aluguel = aluguel_repo.buscar_aluguel_ativo(idCiclista)

    if aluguel:
        return {"id": aluguel.idBicicleta, "numero": aluguel.idBicicleta}

    return {}

@router.get("/ciclista/existeEmail/{email}", response_model=bool)
def existe_email(email: str):
    """Verifica se email já foi utilizado"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)

    return ciclista_repo.buscar_por_email(email) is not None
