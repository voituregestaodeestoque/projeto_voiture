from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_entrada import Pedido_entrada
from models.produto import Produto

class Detalhe_entrada(CrudBase):
    table = "detalhe_entrada"
    fields = [
        'detalhe_entrada_quantidade',
        'produto_id',
        'detalhe_entrada_item',
        'pedido_entrada_id'
    ]

    def __init__(self, detalhe_entrada_quantidade, produto_id, detalhe_entrada_item, pedido_entrada_id ):
        self.detalhe_entrada_quantidade = detalhe_entrada_quantidade
        self.produto_id = produto_id
        self.detalhe_entrada_item = detalhe_entrada_item
        self.pedido_entrada_id = pedido_entrada_id


    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.detalhe_entrada_quantidade, "detalhe_entrada_quantidade"),
            Validator.required(self.produto_id, "produto_id"),
            Validator.required(self.pedido_entrada_id, "pedido_entrada_id"),
        ]

        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def find_by_pedido(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
            SELECT
            detalhe_entrada.id,
            detalhe_entrada.pedido_entrada_id,
            detalhe_entrada.produto_id,
            p.produto_nome AS produto,
            detalhe_entrada.detalhe_entrada_quantidade
            FROM detalhe_entrada
            INNER JOIN produto p
            ON detalhe_entrada.produto_id = p.id
            WHERE detalhe_entrada.pedido_entrada_id = %s
            ORDER BY detalhe_entrada.id
            """
            cursor.execute(sql, (pedido_entrada_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def adicionar_item(cls, detalhe_entrada_quantidade, produto_id,  detalhe_entrada_item, pedido_entrada_id ):
        pedido = Pedido_entrada.find_by_id(pedido_entrada_id)
        
        if not pedido:
            print("01")
            return "Pedido não encontrado."

        if pedido["status_pedido_entrada"] != "PENDENTE":
            print("02")
            return "Não é possível alterar um pedido finalizado."

        produto = Produto.find_by_id(produto_id)

        if not produto:
            return "Produto não encontrado."



        if detalhe_entrada_quantidade <= 0:
            print("04")
            return "A quantidade deve ser maior que zero."

        detalhe = cls(
        detalhe_entrada_quantidade,
        produto_id,
        detalhe_entrada_item,
        pedido_entrada_id
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
    def remover_item(cls, detalhe_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM detalhe_entrada WHERE id = %s",
                (detalhe_entrada_id,)
            )
            item = cursor.fetchone()

            if not item:
                return "Item não encontrado."

            pedido_entrada_id = item["pedido_entrada_id"]

            cursor.execute(
                "DELETE FROM detalhe_entrada WHERE id = %s",
                (detalhe_entrada_id,)
            )
            conexao.commit()

            return "Item removido com sucesso."

        except Exception:
            conexao.rollback()
            return "Erro ao remover item."
        finally:
            cursor.close()
            conexao.close()
