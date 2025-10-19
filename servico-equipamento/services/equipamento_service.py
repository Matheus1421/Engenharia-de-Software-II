from models.status_model import StatusResposta

class EquipamentoService:
    """
    Camada de Serviço responsável pela lógica de negócio do Microsserviço de Equipamentos.
    Por enquanto, contém apenas a lógica para o "Olá Mundo".
    """
    def obter_status_servico(self) -> StatusResposta:
        """
        Retorna uma mensagem de status de "Olá Mundo" para o serviço.
        """
        return StatusResposta(
            mensagem="Olá Mundo! O Microsserviço de Equipamentos está online.",
            status="Operacional"
        )
