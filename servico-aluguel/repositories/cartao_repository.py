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
            "validade": cartao.validade,
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

    def atualizar(self, cartao: NovoCartaoDeCredito, id: int = None, id_ciclista: int = None) -> Optional[CartaoDeCredito]:
        """UC07: Alterar cartão (aceita id ou id_ciclista)"""
        # Se passou id, buscar o idCiclista
        if id is not None:
            cartao_existente = self.buscar_por_id(id)
            if not cartao_existente:
                return None
            id_ciclista = cartao_existente.idCiclista

        if id_ciclista is None:
            return None

        numero_mascarado = "**** **** **** " + cartao.numero[-4:]
        dados = {
            "nomeTitular": cartao.nomeTitular,
            "numero": numero_mascarado,
            "numeroCompleto": cartao.numero,
            "validade": cartao.validade,
            "cvv": cartao.cvv
        }

        self.table.update(dados, self.C.idCiclista == id_ciclista)
        return self.buscar_por_ciclista(id_ciclista)

    def listar(self):
        """Lista todos os cartões"""
        from typing import List
        cartoes = []
        for c in self.table.all():
            c_copy = c.copy()
            c_copy.pop('cvv', None)
            c_copy.pop('numeroCompleto', None)
            cartoes.append(CartaoDeCredito(**c_copy))
        return cartoes

    def buscar_por_id(self, id: int) -> Optional[CartaoDeCredito]:
        """Busca cartão por ID"""
        resultado = self.table.get(self.C.id == id)
        if resultado:
            resultado.pop('cvv', None)
            resultado.pop('numeroCompleto', None)
            return CartaoDeCredito(**resultado)
        return None

    def deletar(self, id: int = None, id_ciclista: int = None) -> bool:
        """Deleta cartão (aceita id ou id_ciclista)"""
        # Se passou id, buscar o idCiclista
        if id is not None:
            cartao_existente = self.buscar_por_id(id)
            if not cartao_existente:
                return False
            id_ciclista = cartao_existente.idCiclista

        if id_ciclista is None:
            return False

        docs_removidos = self.table.remove(self.C.idCiclista == id_ciclista)
        return len(docs_removidos) > 0
