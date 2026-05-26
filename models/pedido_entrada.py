from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Pedido_entrada(CrudBase):
    table = "pedido_entrada"
    fields = [
        'pedidoentrada_status' 
        'pedidoentrada_fornecedor'
    ]

    def __init__(self, pedidoentrada_status, pedidoentrada_fornecedor):
        self.pedidoentrada_produto = pedidoentrada_status
        self.pedidoentrada_fornecedor = pedidoentrada_fornecedor

    
    @classmethod
    def pedido_entrada_join(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "select f.fornecedor_nome, d.detalhe_entrada_quantidade, d.detalhe_entrada_item, p.* from pedido_entrada as p inner join fornecedor as f on p.fornecedor_id = p.fornecedor_id inner join detalhe_entrada as d;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    
    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.pedidoentrada_produto, "pedidoentrada_produto"),
            Validator.required(self.pedidoentrada_fornecedor, "pedidoentrada_fornecedor"),
            Validator.validar_quantidade(self.pedidoentrada_quantidade, "pedidoentrada_quantidade")
        ]

    
    @classmethod
    def find_all_ordered(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM pedido_entrada"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def finalizar(cls, pedidoentrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            conexao.start_transaction()

            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s", (pedidoentrada_id,))
            pedido = cursor.fetchone()

            if not pedido:
                conexao.rollback()
                return "Pedido não encontrado."

            if pedido["status"] != "ABERTO":
                conexao.rollback()
                return "Somente pedidos abertos podem ser finalizados."

            cursor.execute(
                "SELECT * FROM detalhe_entrada WHERE pedido_entrada_id = %s",
                (pedidoentrada_id,)
            )
            itens = cursor.fetchall()

            if not itens:
                conexao.rollback()
                return "Não é possível finalizar um pedido sem itens."

            for item in itens:
                cursor.execute("SELECT * FROM produto WHERE id = %s", (item["produto_id"],))
                produto = cursor.fetchone()

                if not produto:
                    conexao.rollback()
                    return "Produto não encontrado no pedido."

                if item["quantidade"] > produto["quantidade"]:
                    conexao.rollback()
                    return f"Estoque insuficiente para o produto {produto['nome']}."

                nova_quantidade = produto["quantidade"] - item["quantidade"]

                cursor.execute(
                    "UPDATE produto SET quantidade = %s WHERE id = %s",
                    (nova_quantidade, produto["id"])
                )

                cursor.execute(
                    """
                    INSERT INTO movimentacao 
                    (produto_id, tipo_movimentacao, quantidade, data_movimentacao)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (produto["id"], "SAIDA", item["quantidade"], datetime.now())
                )

            cursor.execute(
                """
                UPDATE pedido_entrada
                SET status = %s
                WHERE id = %s
                """,
                ("FINALIZADO", pedido_id)
            )

            conexao.commit()
            return "Pedido de entrada finalizado com sucesso."

        except Exception:
            conexao.rollback()
            return "Erro ao finalizar pedido de entrada."
        finally:
            cursor.close()
            conexao.close()

    