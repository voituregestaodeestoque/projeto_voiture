from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_entrada import Pedido_entrada
from models.estoque import Estoque

class Detalhe_entrada(CrudBase):
    table = "detalhe_entrada"
    fields = [
        'detalhe_entrada_quantidade',
        'estoque_id',
        'detalhe_entrada_item',
        'pedido_entrada_id'
    ]

    def __init__(self, detalhe_entrada_quantidade, estoque_id, pedido_entrada_id,detalhe_entrada_item):
        self.detalhe_entrada_quantidade = detalhe_entrada_quantidade
        self.estoque_id = estoque_id
        self.pedido_entrada_id = pedido_entrada_id
        self.detalhe_entrada_item = detalhe_entrada_item


    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.detalhe_entrada_quantidade, "detalhe_entrada_quantidade"),
            Validator.required(self.estoque_id, "estoque_id"),
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
                detalhe_entrada.estoque_id,
                p.produto_nome AS produto,
                detalhe_entrada.detalhe_entrada_quantidade
            FROM detalhe_entrada
            INNER JOIN estoque e ON detalhe_entrada.estoque_id = e.id
            INNER JOIN produto p ON e.produto_id = p.id
            WHERE detalhe_entrada.pedido_entrada_id = %s
            ORDER BY detalhe_entrada.id
            """
            cursor.execute(sql, (pedido_entrada_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def adicionar_item(cls, detalhe_entrada_quantidade, pedido_entrada_id, produto_id, detalhe_entrada_item):
        pedido = Pedido_entrada.find_by_id(pedido_entrada_id)

        if not pedido:
            return "Pedido não encontrado."

        if pedido["status_pedido_entrada"] != "PENDENTE":
            return "Não é possível alterar um pedido finalizado."

        estoque = Estoque.encontrar_produto(produto_id)

        if not estoque:
            return "Produto não encontrado."

        if detalhe_entrada_quantidade <= 0:
            return "A quantidade deve ser maior que zero."

        detalhe = cls( detalhe_entrada_quantidade, estoque["id"], pedido_entrada_id, produto_id)

        erros = detalhe.validate()
        if erros:
            return erros[0]

        detalhe.insert()

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
