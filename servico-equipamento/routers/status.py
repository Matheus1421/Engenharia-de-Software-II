from fastapi import APIRouter, Depends
from models.status_model import StatusResposta
from services.equipamento_service import EquipamentoService

# Criação do roteador para o endpoint de status
router = APIRouter(
    tags=["Status"],
    prefix="/status"
)

# Injeção de dependência para a camada de serviço
def get_equipamento_service():
    # Retorna uma nova instância do serviço
    return EquipamentoService()

@router.get("/", response_model=StatusResposta)
def obter_status(
    service: EquipamentoService = Depends(get_equipamento_service)
):
    """
    Endpoint de "Olá Mundo" que retorna o status de funcionamento do microsserviço.
    
    Este é o seu primeiro endpoint implementado.
    """
    # A lógica de negócio é delegada à camada de Serviço
    return service.obter_status_servico()
