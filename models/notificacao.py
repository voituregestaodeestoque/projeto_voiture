from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from datetime import datetime

class Notificacao:

    @classmethod
    def verificar_e_gerar(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            ativos = []  # guarda (tipo, referencia_id) de tudo que está em aberto nesta rodada

            # 1. Estoque baixo
            sql_estoque = """
                SELECT p.id AS produto_id, p.produto_nome, e.estoque_quantidade, p.produto_quantidade_minima
                FROM estoque AS e
                INNER JOIN produto AS p ON p.id = e.produto_id
                WHERE e.estoque_quantidade <= p.produto_quantidade_minima * 1.1;
            """
            cursor.execute(sql_estoque)
            for p in cursor.fetchall():
                mensagem = f"{p['produto_nome']} está com estoque baixo ({p['estoque_quantidade']}/{p['produto_quantidade_minima']})"
                ativos.append(('estoque', p['produto_id']))
                cls._inserir_se_nao_existir(cursor, 'estoque', p['produto_id'], mensagem)

            # 2. Pedidos de entrada pendentes
            cursor.execute("SELECT * FROM pedido_entrada WHERE status_pedido_entrada = 'pendente';")
            for pedido in cursor.fetchall():
                mensagem = f"Pedido de entrada nº{pedido['id']} está pendente"
                ativos.append(('entrada', pedido['id']))
                cls._inserir_se_nao_existir(cursor, 'entrada', pedido['id'], mensagem)

            # 3. Pedidos de saída pendentes
            cursor.execute("SELECT * FROM pedido_saida WHERE status_pedido_saida = 'pendente';")
            for pedido in cursor.fetchall():
                mensagem = f"Pedido de saída nº{pedido['id']} está pendente"
                ativos.append(('saida', pedido['id']))
                cls._inserir_se_nao_existir(cursor, 'saida', pedido['id'], mensagem)

            cls._limpar_resolvidas(cursor, ativos)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def _inserir_se_nao_existir(cls, cursor, tipo, referencia_id, mensagem):
        sql = """
            INSERT IGNORE INTO notificacao (notificacao, referencia_id, mensagem)
            VALUES (%s, %s, %s);
        """
        cursor.execute(sql, (tipo, referencia_id, mensagem))

    @classmethod
    def _limpar_resolvidas(cls, cursor, ativos):
        cursor.execute("SELECT id_notificacao, notificacao, referencia_id FROM notificacao;")
        for row in cursor.fetchall():
            chave = (row['notificacao'], row['referencia_id'])
            if chave not in ativos:
                cursor.execute("DELETE FROM notificacao WHERE id_notificacao = %s;", (row['id_notificacao'],))

    @classmethod
    def listar(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM notificacao ORDER BY data_hora DESC;")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def deletar(cls, id_notificacao):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM notificacao WHERE id_notificacao = %s;", (id_notificacao,))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def deletar_todas(cls):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM notificacao;")
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()