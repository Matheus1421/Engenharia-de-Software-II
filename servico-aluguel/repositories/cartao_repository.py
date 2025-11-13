from typing import Optional
from tinydb import TinyDB, Query
from models.cartao_model import NovoCartaoDeCredito, CartaoDeCredito

class CartaoRepository:
    def __init__(self, db: TinyDB):
        self.table = db.table('cartoes')
        self.C = Query()

    def criar(self, id_ciclista: int, cartao: NovoCartaoDeCredito) -> CartaoDeCredito:
        """UC01: Cadastrar cartão do ciclista"""
        todos = self.table.all()
        proximo_id = max([c.get('id', 0) for c in todos], default=0) + 1

        # Mascara o número antes de salvar (segurança)
        numero_mascarado = "**** **** **** " + cartao.numero[-4:]

        dados = {
            "id": proximo_id,
            "idCiclista": id_ciclista,
            "nomeTitular": cartao.nomeTitular,
            "numero": numero_mascarado,
            "numeroCompleto": cartao.numero, 
            "validade": cartao.validade.isoformat(),
            "cvv": cartao.cvv
        }

        self.table.insert(dados)
        return CartaoDeCredito(**{k: v for k, v in dados.items() if k != 'numeroCompleto'})

    def buscar_por_ciclista(self, id_ciclista: int) -> Optional[CartaoDeCredito]:
        resultado = self.table.get(self.C.idCiclista == id_ciclista)
        if resultado:
            # Remove campos sensíveis ao retornar
            resultado.pop('cvv', None)
            resultado.pop('numeroCompleto', None)
            return CartaoDeCredito(**resultado)
        return None

    def atualizar(self, id_ciclista: int, cartao: NovoCartaoDeCredito) -> Optional[CartaoDeCredito]:
        """UC07: Alterar cartão"""
        numero_mascarado = "**** **** **** " + cartao.numero[-4:]
        dados = {
            "nomeTitular": cartao.nomeTitular,
            "numero": numero_mascarado,
            "numeroCompleto": cartao.numero,
            "validade": cartao.validade.isoformat(),
            "cvv": cartao.cvv
        }

        self.table.update(dados, self.C.idCiclista == id_ciclista)
        return self.buscar_por_ciclista(id_ciclista)
