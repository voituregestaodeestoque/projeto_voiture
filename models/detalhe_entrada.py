from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_entrada import Pedido_entrada

class Detalhe_entrada(CrudBase):
    table = "detalhe_entrada"
    fields = [
        'detalhe_entrada_quantidade'
    ]

    def __init__(self, detalhe_entrada_quantidade):
        self.detalhe_entrada_quantidade = detalhe_entrada_quantidade

    
    @classmethod
    def find_by_pedido(cls, pedido_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
            SELECT 
                detalhe_entrada.id,
                detalhe_entrada.pedidoentrada_id,
                detalhe_entrada.estoque_id,
                p.produto_nome AS produto,
                detalhe_entrada.quantidade
            FROM detalhe_entrada
            INNER JOIN produto p ON detalhe_entrada.produto_id = p.id
            WHERE detalhe_entrada.pedidoentrada_id = %s
            ORDER BY detalhe_entrada.id
            """
            cursor.execute(sql, (pedido_entrada_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def adicionar_item(cls, pedido_entrada_id, produto_id, quantidade):
        pedido = PedidoEntrada.find_by_id(pedido_entrada_id)

        if not pedido:
            return "Pedido não encontrado."

        if pedido["status"] != "ABERTO":
            return "Não é possível alterar um pedido finalizado."

        produto = Produto.find_by_id(produto_id)

        if not produto:
            return "Produto não encontrado."

        if quantidade <= 0:
            return "A quantidade deve ser maior que zero."

        detalhe = cls(
            pedidoentrada_id=pedido_entrada_id,
            produto_id=produto_id,
            quantidade=quantidade
        )

        erros = detalhe.validate()
        if erros:
            return erros[0]

        detalhe.insert()
        Pedido_entrada.atualizar_total(pedido_entrada_id)

        return "Item adicionado ao pedido."

    @classmethod
    def remover_item(cls, detalhe_entrada_id_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM detalhe_entrada WHERE id = %s",
                (item_id,)
            )
            item = cursor.fetchone()

            if not item:
                return "Item não encontrado."

            pedido_entrada_id = detalhe["pedido_entrada_id"]

            cursor.execute(
                "DELETE FROM detalhe_entrada WHERE id = %s",
                (detalhe_entrada_id,)
            )
            conexao.commit()

            Pedido_entrada.atualizar_total(pedido_entrada_id)

            return "Item removido com sucesso."

        except Exception:
            conexao.rollback()
            return "Erro ao remover item."
        finally:
            cursor.close()
            conexao.close()
