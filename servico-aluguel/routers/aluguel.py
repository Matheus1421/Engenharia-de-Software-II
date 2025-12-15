"""ROUTER: Aluguel e Devolução - UC03, UC04"""

from fastapi import APIRouter, HTTPException
from models.aluguel_model import NovoAluguel, Aluguel, NovaDevolucao, Devolucao
from repositories.ciclista_repository import CiclistaRepository
from repositories.aluguel_repository import AluguelRepository
from services.equipamento_service import equipamento_service
from services.email_service import email_service
from services.pagamento_service import pagamento_service
from database.database import get_db
from datetime import datetime

router = APIRouter(prefix="", tags=["Aluguel"])

@router.post("/aluguel", response_model=Aluguel)
def alugar_bicicleta(dados: NovoAluguel):
    """UC03: Alugar Bicicleta"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)
    aluguel_repo = AluguelRepository(db)

    # UC03 - R1: Verificar se ciclista pode alugar
    if not ciclista_repo.pode_alugar(dados.ciclista):
        raise HTTPException(status_code=422, detail="Ciclista não pode alugar")

    if aluguel_repo.buscar_aluguel_ativo(dados.ciclista):
        raise HTTPException(status_code=422, detail="Ciclista já possui um aluguel ativo")

    # UC03 - Passo 4: Ler bicicleta na tranca
    sucesso_bicicleta, bicicleta = equipamento_service.obter_bicicleta_tranca(dados.trancaInicio)

    if not sucesso_bicicleta or not bicicleta:
        raise HTTPException(status_code=422, detail="Não há bicicleta na tranca informada")

    # UC03 - Passo 6: Cobrar R$ 10,00
    sucesso_cobranca, cobranca_resultado = pagamento_service.cobrar(10.00, dados.ciclista, "Aluguel SCB")

    if not sucesso_cobranca or cobranca_resultado.get("status") != "PAGA":
        raise HTTPException(status_code=422, detail="Pagamento não autorizado")

    cobranca = aluguel_repo.criar_cobranca(10.00, dados.ciclista, "ALUGUEL_INICIAL")

    # UC03 - Passo 10: Destrancar
    sucesso_destrancar, _ = equipamento_service.destrancar(dados.trancaInicio, bicicleta['id'])
    if not sucesso_destrancar:
        raise HTTPException(status_code=500, detail="Erro ao destrancar tranca")

    # UC03 - Passo 8: Registrar aluguel
    aluguel = aluguel_repo.criar_aluguel(
        dados.ciclista,
        dados.trancaInicio,
        bicicleta['id'],
        cobranca.id
    )

    # UC03 - Passo 11: Enviar email
    ciclista = ciclista_repo.buscar_por_id(dados.ciclista)
    sucesso_email, _ = email_service.enviar_recibo_aluguel(
        ciclista.email,
        ciclista.nome,
        bicicleta['id'],
        dados.trancaInicio,
        10.00,
        aluguel.horaInicio
    )
    if not sucesso_email:
        print(f"Aviso: Falha ao enviar email de confirmacao de aluguel para {ciclista.email}")

    return aluguel

@router.post("/devolucao", response_model=Devolucao)
def devolver_bicicleta(dados: NovaDevolucao):
    """UC04: Devolver Bicicleta"""
    db = get_db()
    ciclista_repo = CiclistaRepository(db)
    aluguel_repo = AluguelRepository(db)

    # Buscar aluguel ativo da bicicleta
    todos_alugueis = db.table('alugueis').all()
    aluguel_dict = None

    for a in todos_alugueis:
        if a['bicicleta'] == dados.idBicicleta and a['status'] == 'EM_ANDAMENTO':
            aluguel_dict = a
            break

    if not aluguel_dict:
        raise HTTPException(status_code=422, detail="Não há aluguel ativo para esta bicicleta")

    # UC04 - Passo 3: Calcular tempo
    hora_inicio = datetime.fromisoformat(aluguel_dict['horaInicio'])
    hora_fim = datetime.now()
    tempo_minutos = int((hora_fim - hora_inicio).total_seconds() / 60)

    # UC04 - R1: Calcular taxa extra (R$ 5,00 por meia hora após 2 horas)
    taxa_extra = 0.0
    if tempo_minutos > 120:
        minutos_extras = tempo_minutos - 120
        meias_horas_extras = (minutos_extras + 29) // 30
        taxa_extra = meias_horas_extras * 5.00

    # Cobrar taxa extra se houver
    id_cobranca_extra = None
    if taxa_extra > 0:
        cobranca_extra = aluguel_repo.criar_cobranca(
            taxa_extra,
            aluguel_dict['ciclista'],
            "TAXA_EXTRA"
        )
        id_cobranca_extra = cobranca_extra.id

    # UC04 - Passo 6: Trancar
    sucesso_trancar, _ = equipamento_service.trancar(dados.idTranca, dados.idBicicleta)
    if not sucesso_trancar:
        raise HTTPException(status_code=500, detail="Erro ao trancar tranca")

    # UC04 - Passo 4: Finalizar aluguel
    aluguel = aluguel_repo.finalizar_aluguel(
        aluguel_dict['id'],
        dados.idTranca,
        id_cobranca_extra
    )

    # UC04 - Passo 7: Enviar email
    ciclista = ciclista_repo.buscar_por_id(aluguel.ciclista)
    sucesso_email, _ = email_service.enviar_recibo_devolucao(
        ciclista.email,
        ciclista.nome,
        dados.idBicicleta,
        dados.idTranca,
        tempo_minutos,
        10.00 + taxa_extra,
        taxa_extra
    )
    if not sucesso_email:
        print(f"Aviso: Falha ao enviar email de confirmacao de devolucao para {ciclista.email}")

    return Devolucao(
        aluguel=aluguel,
        valorTotal=10.00 + taxa_extra,
        tempoTotal=tempo_minutos,
        taxaExtra=taxa_extra
    )
