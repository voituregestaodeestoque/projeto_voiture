from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from datetime import datetime

class Pedido_entrada(CrudBase):
    table = "pedido_entrada"
    fields = [
        'status_pedido_entrada', 
        'fornecedor_id'
    ]

    def __init__(self, status_pedido_entrada, fornecedor_id):
        self.status_pedido_entrada = status_pedido_entrada
        self.fornecedor_id = fornecedor_id

    
    @classmethod
    def pedido_entrada_join(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """select f.fornecedor_nome, d.detalhe_entrada_quantidade, d.detalhe_entrada_item, p.* from pedido_entrada as p 
            INNER JOIN fornecedor as f 
            ON p.fornecedor_id = f.id 
            INNER JOIN detalhe_entrada d 
            ON p.id = d.pedido_entrada_id;"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    
    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.status_pedido_entrada, "status_pedido_entrada"),
            Validator.required(self.fornecedor_id, "fornecedor_id")
        ]

        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    
    @classmethod
    def find_all_ordered(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """SELECT 
                    p.id, 
                    p.status_pedido_entrada, 
                    p.fornecedor_id, 
                    MAX(m.datahora_movimentacao_entrada) AS data_processamento
                FROM pedido_entrada p
                LEFT JOIN detalhe_entrada de ON p.id = de.pedido_entrada_id
                LEFT JOIN movimentacao_entrada m ON de.id = m.detalhe_entrada_id 
                    AND de.pedido_entrada_id = m.detalhe_entrada_pedido_entrada_id
                GROUP BY p.id, p.status_pedido_entrada, p.fornecedor_id
                ORDER BY p.id DESC"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def finalizar(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            conexao.start_transaction()

            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s", (pedido_entrada_id,))
            pedido = cursor.fetchone()

            if not pedido:
                conexao.rollback()
                return "Pedido não encontrado."

            if pedido["status_pedido_entrada"] != "PENDENTE":
                conexao.rollback()
                return "Somente pedidos abertos podem ser finalizados."

            cursor.execute(
                "SELECT * FROM detalhe_entrada WHERE pedido_entrada_id = %s",
                (pedido_entrada_id,)
            )
            itens = cursor.fetchall()

            if not itens:
                conexao.rollback()
                return "Não é possível finalizar um pedido sem itens."

            for item in itens:

                produto_id = item["detalhe_entrada_item"]
                quantidade = item["detalhe_entrada_quantidade"]

                cursor.execute(
                "SELECT * FROM estoque WHERE id = %s",
                    (item["estoque_id"],))

                estoque = cursor.fetchone()
                if not estoque:
                    conexao.rollback()
                    return "Produto não encontrado no pedido."

                nova_quantidade = estoque["estoque_quantidade"] + item["detalhe_entrada_quantidade"]

                cursor.execute(
                """ 
                    UPDATE estoque
                    SET estoque_quantidade = %s
                    WHERE id = %s
                    """,
                    (nova_quantidade, item["estoque_id"]) )

                cursor.execute(
                    """
                    INSERT INTO movimentacao_entrada 
                    (datahora_movimentacao_entrada, detalhe_entrada_id, detalhe_entrada_pedido_entrada_id)
                    VALUES (%s, %s, %s)
                    """,
                    (datetime.now(), item["id"], pedido_entrada_id)
                )

            cursor.execute(
                """
                UPDATE pedido_entrada
                SET status_pedido_entrada = %s
                WHERE id = %s
                """,
                ("FINALIZADO", pedido_entrada_id)
            )

            conexao.commit()
            return "Pedido de entrada finalizado com sucesso."

        except Exception:
            conexao.rollback()
            return "Erro ao finalizar pedido de entrada."
        finally:
            cursor.close()
            conexao.close()

    
    @classmethod
    def find_by_id(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            # Faz o JOIN para trazer a coluna "fornecedor" que o seu HTML precisa
            sql = """SELECT 
                        p.id, 
                        p.status_pedido_entrada, 
                        p.fornecedor_id,
                        f.fornecedor_nome AS fornecedor
                    FROM pedido_entrada p
                    INNER JOIN fornecedor f ON p.fornecedor_id = f.id
                    WHERE p.id = %s"""
            cursor.execute(sql, (pedido_entrada_id,))
            return cursor.fetchone() # Retorna o pedido com o nome do fornecedor incluso
        finally:
            cursor.close()
            conexao.close()

    