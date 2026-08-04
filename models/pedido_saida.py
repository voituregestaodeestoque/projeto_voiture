from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from datetime import datetime

class Pedido_saida(CrudBase):
    table = "pedido_saida"
    fields = [
        'status_pedido_saida', 
        'cliente_id',
        'data_pedido_saida' 
    ]

    def __init__(self, status_pedido_saida, cliente_id, data_pedido_saida):
        self.status_pedido_saida = status_pedido_saida
        self.cliente_id = cliente_id
        self.data_pedido_saida = data_pedido_saida

    
    @classmethod
    def pedido_saida_join(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """select c.cliente_nome, d.detalhe_saida_quantidade, d.detalhe_saida_item, p.* from pedido_saida as p 
            INNER JOIN cliente as c 
            ON p.cliente_id = c.id 
            INNER JOIN detalhe_saida d 
            ON p.id = d.pedido_saida_id;"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.status_pedido_saida, "status_pedido_saida"),
            Validator.required(self.cliente_id, "cliente_id")
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
            sql = """SELECT p.id as pedido_saida_id, p.status_pedido_saida, p.data_pedido_saida, p.cliente_id, pr.produto_nome, de.detalhe_saida_quantidade, 
                MAX(m.datahora_movimentacao_saida) AS data_processamento
                FROM pedido_saida p
                LEFT JOIN detalhe_saida de ON p.id = de.pedido_saida_id
                LEFT JOIN movimentacao_saida m ON de.id = m.detalhe_saida_id AND de.pedido_saida_id = m.detalhe_saida_pedido_saida_id
                LEFT JOIN estoque e ON de.produto_id = e.id
                LEFT JOIN produto pr ON e.produto_id = pr.id
                GROUP BY p.id, p.status_pedido_saida, p.cliente_id, pr.produto_nome, de.detalhe_saida_quantidade
                ORDER BY p.id desc"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def finalizar(cls, pedido_saida_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            conexao.start_transaction()

            cursor.execute("SELECT * FROM pedido_saida WHERE id = %s", (pedido_saida_id,))
            pedido = cursor.fetchone()

            if not pedido:
                conexao.rollback()
                return "Pedido não encontrado."

            if pedido["status_pedido_saida"] != "PENDENTE":
                conexao.rollback()
                return "Somente pedidos abertos podem ser finalizados."

            cursor.execute(
                "SELECT * FROM detalhe_saida WHERE pedido_saida_id = %s",
                (pedido_saida_id,)
            )
            itens = cursor.fetchall()

            if not itens:
                conexao.rollback()
                return "Não é possível finalizar um pedido sem itens."

            for item in itens:
                cursor.execute(
                    "SELECT * FROM estoque WHERE id = %s",
                    (item["estoque_id"],)
                )
                estoque = cursor.fetchone()
                
                if not estoque:
                    conexao.rollback()
                    return "Produto não encontrado no pedido."

                #Verificar se há estoque suficiente
                if estoque["estoque_quantidade"] < item["detalhe_saida_quantidade"]:
                    conexao.rollback()
                    return f"Estoque insuficiente para o item {item['produto_id']}."

                
                nova_quantidade = estoque["estoque_quantidade"] - item["detalhe_saida_quantidade"]

                cursor.execute(
                    """ 
                    UPDATE estoque
                    SET estoque_quantidade = %s
                    WHERE id = %s
                    """,
                    (nova_quantidade, item["produto_id"]) 
                )

                cursor.execute(
                    """
                    INSERT INTO movimentacao_saida 
                    (datahora_movimentacao_saida, detalhe_saida_id, detalhe_saida_pedido_saida_id)
                    VALUES (%s, %s, %s)
                    """,
                    (datetime.now(), item["id"], pedido_saida_id)
                )

            conexao.commit()
            return "Pedido de saída finalizado com sucesso."

        finally:
            cursor.close()
            conexao.close()

    

    
    @classmethod
    def find_by_id(cls, pedido_saida_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """SELECT 
                        p.id, 
                        p.status_pedido_saida,
                        p.data_pedido_saida, 
                        p.cliente_id,
                        c.cliente_nome AS cliente
                    FROM pedido_saida p
                    INNER JOIN cliente c ON p.cliente_id = c.id
                    WHERE p.id = %s"""
            cursor.execute(sql, (pedido_saida_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def processar(cls, pedido_saida_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            conexao.start_transaction()

            cursor.execute("SELECT * FROM pedido_saida WHERE id = %s FOR UPDATE", (pedido_saida_id,))
            pedido = cursor.fetchone()
            if not pedido:
                raise ValueError("Pedido de saída não encontrado.")

            if pedido["status_pedido_saida"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser processados.")

            cursor.execute("SELECT * FROM detalhe_saida WHERE pedido_saida_id = %s FOR UPDATE", (pedido_saida_id,))

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
                
                if estoque['estoque_quantidade'] < detalhe["detalhe_saida_quantidade"]:
                    raise ValueError (
                        f"Estoque insuficiente para o produto {detalhe['produto_id']}"
                    )

                nova_quantidade = (
                    estoque["estoque_quantidade"] - detalhe["detalhe_saida_quantidade"]
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
                    INSERT INTO movimentacao_saida
                    (
                        datahora_movimentacao_saida,
                        detalhe_saida_id,
                        detalhe_saida_pedido_saida_id
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        datetime.now(),
                        detalhe["id"],
                        pedido_saida_id,
                    )
                )

    
            cursor.execute(
                """
                UPDATE pedido_saida
                SET status_pedido_saida = %s
                WHERE id = %s
                """,
                ("CONCLUIDO", pedido_saida_id,)
            )

            conexao.commit()
            return "Pedido de saída processado com sucesso."
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def cancelar(cls, pedido_saida_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pedido_saida WHERE id = %s", (pedido_saida_id,))
            pedido = cursor.fetchone()
            if not pedido:
                raise ValueError("Pedido de saída não encontrado.")
            if pedido["status_pedido_saida"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser cancelados.")

            cursor = conexao.cursor()
            cursor.execute(
                """
                UPDATE pedido_saida
                SET status_pedido_saida = %s
                WHERE id = %s
                """,
                ("CANCELADO", pedido_saida_id,)
            )
            conexao.commit()
            return "Pedido de saída cancelado com sucesso."
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def contar_pedidosaida(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT COUNT(status_pedido_saida) as pedido_saida_total FROM pedido_saida WHERE status_pedido_saida = 'pendente';"
            cursor.execute(sql)
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def pedidosaida_pendente(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM pedido_saida WHERE status_pedido_saida = 'pendente';"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    @classmethod
    def total_saidas(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT 
                SUM(detalhe_saida_quantidade) AS total
            FROM detalhe_saida
            """

            cursor.execute(sql)
            resultado = cursor.fetchone()

            return resultado["total"] or 0

        finally:
            cursor.close()
            conexao.close()