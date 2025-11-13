"""ROUTER: Cartão de Crédito - UC07"""

from fastapi import APIRouter, HTTPException, Query as QueryParam
from typing import List
from models.cartao_model import CartaoDeCredito, NovoCartaoDeCredito
from repositories.cartao_repository import CartaoRepository
from services.pagamento_service import pagamento_service
from database.database import get_db

router = APIRouter(prefix="/cartao", tags=["Cartão de Crédito"])

@router.get("", response_model=List[CartaoDeCredito])
def listar_cartoes():
    """Lista todos os cartões"""
    db = get_db()
    repo = CartaoRepository(db)
    return repo.listar()

@router.get("/{id}", response_model=CartaoDeCredito)
def obter_cartao_por_id(id: int):
    """Recupera cartão por ID"""
    db = get_db()
    repo = CartaoRepository(db)

    cartao = repo.buscar_por_id(id)
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    return cartao

@router.get("/ciclista/{idCiclista}", response_model=CartaoDeCredito)
def obter_cartao_por_ciclista(idCiclista: int):
    """Recupera cartão do ciclista"""
    db = get_db()
    repo = CartaoRepository(db)

    cartao = repo.buscar_por_ciclista(idCiclista)
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    return cartao

@router.post("", response_model=CartaoDeCredito, status_code=201)
def cadastrar_cartao(cartao: NovoCartaoDeCredito, idCiclista: int = QueryParam(...)):
    """Cadastra um novo cartão para o ciclista"""
    db = get_db()
    repo = CartaoRepository(db)

    # Validar cartão com administradora
    validacao = pagamento_service.validar_cartao(
        cartao.numero,
        cartao.nomeTitular,
        cartao.validade,
        cartao.cvv
    )

    if not validacao.get("valido"):
        raise HTTPException(status_code=422, detail="Cartão inválido")

    return repo.criar(idCiclista, cartao)

@router.put("/{id}", response_model=CartaoDeCredito)
def alterar_cartao_por_id(id: int, cartao: NovoCartaoDeCredito):
    """UC07: Alterar dados de cartão de crédito por ID"""
    db = get_db()
    repo = CartaoRepository(db)

    # Validar novo cartão
    validacao = pagamento_service.validar_cartao(
        cartao.numero,
        cartao.nomeTitular,
        cartao.validade,
        cartao.cvv
    )

    if not validacao.get("valido"):
        raise HTTPException(status_code=422, detail="Cartão inválido")

    cartao_atualizado = repo.atualizar(cartao, id=id)
    if not cartao_atualizado:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    return cartao_atualizado

@router.delete("/{id}", status_code=200)
def deletar_cartao(id: int):
    """Deleta cartão por ID"""
    db = get_db()
    repo = CartaoRepository(db)

    sucesso = repo.deletar(id=id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    return {"message": "Cartão deletado com sucesso"}
