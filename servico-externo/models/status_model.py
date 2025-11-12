from pydantic import BaseModel

# O modelo define a estrutura dos dados que serão enviados na resposta HTTP.
class StatusResposta(BaseModel):
    """
    Define a estrutura da resposta para o status de "Olá Mundo".
    """
    mensagem: str
    status: str

