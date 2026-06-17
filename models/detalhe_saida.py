from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_saida import Pedido_saida
from models.produto import Produto

class Detalhe_saida(CrudBase):
    table = "detalhe_saida"
    fields = [
        'detalhe_saida_quantidade',
        'produto_id',
        'detalhe_saida_item',
        'pedido_saida_id'
    ]

    def __init__(self, detalhe_saida_quantidade, produto_id, detalhe_saida_item, pedido_saida_id):
        self.detalhe_saida_quantidade = detalhe_saida_quantidade
        self.produto_id = produto_id
        self.detalhe_saida_item = detalhe_saida_item
        self.pedido_saida_id = pedido_saida_id


    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.detalhe_saida_quantidade, "detalhe_saida_quantidade"),
            Validator.required(self.produto_id, "produto_id"),
            Validator.required(self.pedido_saida_id, "pedido_saida_id"),
        ]

        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def find_by_pedido(cls, pedido_saida_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
            SELECT
            detalhe_saida.id,
            detalhe_saida.pedido_saida_id,
            detalhe_saida.produto_id,
            p.produto_nome AS produto,
            detalhe_saida.detalhe_saida_quantidade
            FROM detalhe_saida
            INNER JOIN produto p
            ON detalhe_saida.produto_id = p.id
            WHERE detalhe_saida.pedido_saida_id = %s
            ORDER BY detalhe_saida.id
            """
            cursor.execute(sql, (pedido_saida_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def adicionar_item(cls, detalhe_saida_quantidade, produto_id, detalhe_saida_item, pedido_saida_id):
        print("pedido", pedido_saida_id)
        pedido = Pedido_saida.find_by_id(pedido_saida_id)
        
        if not pedido:
            print("01")
            return "Pedido não encontrado."

        if pedido["status_pedido_saida"] != "PENDENTE":
            print("02")
            return "Não é possível alterar um pedido finalizado."

        produto = Produto.find_by_id(produto_id)
        if not produto:
            return "Produto não encontrado."

        if detalhe_saida_quantidade <= 0:
            print("04")
            return "A quantidade deve ser maior que zero."

        detalhe = cls(
            detalhe_saida_quantidade,
            produto_id,
            detalhe_saida_item,
            pedido_saida_id
        )
        print("detalhe", detalhe)
        erros = detalhe.validate()
        if erros:
            print("05")
            return erros[0]
        
        detalhe.insert()
        print("detalhe ok")
        return "Item adicionado ao pedido."

    @classmethod
    def remover_item(cls, detalhe_saida_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM detalhe_saida WHERE id = %s",
                (detalhe_saida_id,)
            )
            item = cursor.fetchone()

            if not item:
                return "Item não encontrado."

            pedido_saida_id = item["pedido_saida_id"]

            cursor.execute(
                "DELETE FROM detalhe_saida WHERE id = %s",
                (detalhe_saida_id,)
            )
            conexao.commit()

            return "Item removido com sucesso."

        except Exception:
            conexao.rollback()
            return "Erro ao remover item."
        finally:
            cursor.close()
            conexao.close()

    