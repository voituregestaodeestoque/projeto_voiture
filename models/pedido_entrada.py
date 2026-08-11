from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from datetime import datetime

class Pedido_entrada(CrudBase):
    table = "pedido_entrada"
    fields = [
        'status_pedido_entrada', 
        'fornecedor_id',
        'data_pedido_entrada'
    ]

    def __init__(self, status_pedido_entrada, fornecedor_id, data_pedido_entrada):
        self.status_pedido_entrada = status_pedido_entrada
        self.fornecedor_id = fornecedor_id
        self.data_pedido_entrada = data_pedido_entrada

    
    @classmethod
    def pedido_entrada_join(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """select f.fornecedor_nome, d.detalhe_entrada_quantidade, d.detalhe_entrada_item, me.datahora_movimentacao_entrada, p.* from pedido_entrada as p 
            INNER JOIN fornecedor as f 
            ON p.fornecedor_id = f.id 
            INNER JOIN detalhe_entrada d 
            ON p.id = d.pedido_entrada_id
            INNER JOIN movimentacao_entrada me
            ON p.id = me.detalhe_entrada_pedido_entrada_id;"""
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
            sql = """SELECT p.id as pedido_entrada_id, p.status_pedido_entrada, p.data_pedido_entrada, p.fornecedor_id, pr.produto_nome, de.detalhe_entrada_quantidade, 
                    MAX(me.datahora_movimentacao_entrada) AS data_processamento
                    FROM pedido_entrada p
                    LEFT JOIN detalhe_entrada de ON p.id = de.pedido_entrada_id
                    LEFT JOIN movimentacao_entrada me ON de.id = me.detalhe_entrada_id AND de.pedido_entrada_id = me.detalhe_entrada_pedido_entrada_id
                    LEFT JOIN estoque e ON de.produto_id = e.id
                    LEFT JOIN produto pr ON e.produto_id = pr.id
                    GROUP BY p.id, p.status_pedido_entrada, p.fornecedor_id, pr.produto_nome, de.detalhe_entrada_quantidade
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

                cursor.execute(
                """
                SELECT *
                FROM estoque
                WHERE produto_id = %s
                """,
                (item["produto_id"],))

                estoque = cursor.fetchone()
                if not estoque:
                    conexao.rollback()
                    return "Produto não encontrado no pedido."

                nova_quantidade = estoque["estoque_quantidade"] + item["detalhe_entrada_quantidade"]

                cursor.execute(
                """ 
                    UPDATE estoque
                    SET estoque_quantidade = %s
                    WHERE produto_id = %s
                    """,
                    (nova_quantidade, item["produto_id"]) )
                
            conexao.commit()
            return "Pedido de entrada atualizado com sucesso."

        except Exception:
            conexao.rollback()
            return "Erro ao atualizar pedido de entrada."
        finally:
            cursor.close()
            conexao.close()

    
    @classmethod
    def find_by_id(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """SELECT 
                        p.id, 
                        p.status_pedido_entrada,
                        p.data_pedido_entrada, 
                        p.fornecedor_id,
                        f.fornecedor_nome AS fornecedor
                    FROM pedido_entrada p
                    INNER JOIN fornecedor f ON p.fornecedor_id = f.id
                    WHERE p.id = %s"""
            cursor.execute(sql, (pedido_entrada_id,))
            return cursor.fetchone() 
        finally:
            cursor.close()
            conexao.close()

    
    @classmethod
    def processar(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            conexao.start_transaction()

            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s FOR UPDATE", (pedido_entrada_id,))
            pedido = cursor.fetchone()
            if not pedido:
                raise ValueError("Pedido de entrada não encontrado.")

            if pedido["status_pedido_entrada"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser processados.")

            cursor.execute("SELECT * FROM detalhe_entrada WHERE pedido_entrada_id = %s FOR UPDATE", (pedido_entrada_id,))

            detalhes = cursor.fetchall()

            if not detalhes:
                raise ValueError("Pedido sem itens.")

            for detalhe in detalhes:

         
                cursor.execute(
                    """
                    SELECT *
                    FROM estoque
                    WHERE produto_id = %s
                    FOR UPDATE
                    """,
                    (detalhe["produto_id"],)
                )
                estoque = cursor.fetchone()

                if not estoque:
                    raise ValueError(
                        f"Não existe estoque para o produto {detalhe['produto_id']}"
                    )

                nova_quantidade = (
                    estoque["estoque_quantidade"]
                    + detalhe["detalhe_entrada_quantidade"]
                )                
         
                cursor.execute(
                    """
                    UPDATE estoque
                    SET estoque_quantidade = %s
                    WHERE produto_id = %s
                    """,
                    (
                        nova_quantidade,
                        detalhe["produto_id"]
                        )
                )

            
                cursor.execute(
                    """
                    INSERT INTO movimentacao_entrada
                    (
                        datahora_movimentacao_entrada,
                        detalhe_entrada_id,
                        detalhe_entrada_pedido_entrada_id
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        datetime.now(),
                        detalhe["id"],
                        pedido_entrada_id,
                    )
                )

    
            cursor.execute(
                """
                UPDATE pedido_entrada
                SET status_pedido_entrada = %s
                WHERE id = %s
                """,
                ("CONCLUIDO", pedido_entrada_id,)
            )

            conexao.commit()
            return "Pedido de entrada processado com sucesso."
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def cancelar(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s", (pedido_entrada_id,))
            pedido = cursor.fetchone()
            if not pedido:
                raise ValueError("Pedido de entrada não encontrado.")
            if pedido["status_pedido_entrada"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser cancelados.")

            cursor = conexao.cursor()
            cursor.execute(
                """
                UPDATE pedido_entrada
                SET status_pedido_entrada = %s
                WHERE id = %s
                """,
                ("CANCELADO", pedido_entrada_id,)
            )
            conexao.commit()
            return "Pedido de entrada cancelado com sucesso."
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def pedidoentrada_pendente(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM pedido_entrada WHERE status_pedido_entrada = 'pendente';"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def contar_pedidoentrada(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT COUNT(status_pedido_entrada) as pedido_entrada_total FROM pedido_entrada WHERE status_pedido_entrada = 'pendente';"
            cursor.execute(sql)
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()
    @classmethod
    def total_entradas(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT SUM(ds.detalhe_entrada_quantidade) AS total
                FROM detalhe_entrada ds
                INNER JOIN pedido_entrada ps
                    ON ds.pedido_entrada_id = ps.id
                WHERE ps.status_pedido_entrada = 'CONCLUIDO'
            """

            cursor.execute(sql)
            resultado = cursor.fetchone()

            return resultado["total"] or 0

        finally:
            cursor.close()
            conexao.close()