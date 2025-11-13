"""ROUTER: Cartão de Crédito - UC07"""
from fastapi import APIRouter, HTTPException
from models.cartao_model import CartaoDeCredito, NovoCartaoDeCredito
from repositories.cartao_repository import CartaoRepository
from services.pagamento_service import pagamento_service
from database.database import get_db

router = APIRouter(prefix="/cartaoDeCredito", tags=["Cartão de Crédito"])

@router.get("/{idCiclista}", response_model=CartaoDeCredito)
def obter_cartao(idCiclista: int):
    """Recupera dados do cartão (mascarado)"""
    db = get_db()
    repo = CartaoRepository(db)

    cartao = repo.buscar_por_ciclista(idCiclista)

    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    return cartao

@router.put("/{idCiclista}", response_model=CartaoDeCredito)
def alterar_cartao(idCiclista: int, cartao: NovoCartaoDeCredito):
    """UC07: Alterar dados de cartão de crédito"""
    db = get_db()
    repo = CartaoRepository(db)

    # Validar cartão com administradora
    validacao = pagamento_service.validar_cartao(
        cartao.numero,
        cartao.nomeTitular,
        cartao.validade.isoformat(),
        cartao.cvv
    )

    if not validacao.get("valido"):
        raise HTTPException(status_code=422, detail="Cartão inválido")

    cartao_atualizado = repo.atualizar(idCiclista, cartao)

    if not cartao_atualizado:
        raise HTTPException(status_code=404, detail="Ciclista não encontrado")

    return cartao_atualizado
