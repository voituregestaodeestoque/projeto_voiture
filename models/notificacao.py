#importações de tudo que vai ser usado no arquivo
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from datetime import datetime

class Notificacao: 

    @classmethod
    def verificar_e_gerar(cls): #verifica o banco procurando situações que precisam gerar notificações
        conexao = Database.connect() #conectando no banco
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
            for p in cursor.fetchall():#passa por cada produto encontrado.
                mensagem = f"{p['produto_nome']} está com estoque baixo ({p['estoque_quantidade']}/{p['produto_quantidade_minima']})"
                ativos.append(('estoque', p['produto_id']))#adiciona no ativos
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
        # Comando SQL para inserir uma nova notificação
        # O INSERT IGNORE evita erro caso a notificação já exista
        sql = """
            INSERT IGNORE INTO notificacao (notificacao, referencia_id, mensagem)
            VALUES (%s, %s, %s);
        """

        # Executa o comando SQL passando os valores recebidos
        # tipo = tipo da notificação
        # referencia_id = ID relacionado à notificação
        # mensagem = texto que será exibido
        cursor.execute(sql, (tipo, referencia_id, mensagem))


    @classmethod
    def _limpar_resolvidas(cls, cursor, ativos):
        # Busca todas as notificações que estão atualmente no banco
        cursor.execute(
            "SELECT id_notificacao, notificacao, referencia_id FROM notificacao;"
        )

        # Percorre todas as notificações encontradas
        for row in cursor.fetchall():

            # Cria uma chave com o tipo e o ID da notificação
            chave = (row['notificacao'], row['referencia_id'])

            # Verifica se essa notificação ainda está ativa
            # Se não estiver, significa que o problema foi resolvido
            if chave not in ativos:

                # Apaga a notificação resolvida do banco
                cursor.execute(
                    "DELETE FROM notificacao WHERE id_notificacao = %s;",
                    (row['id_notificacao'],)
                )


    @classmethod
    def listar(cls):
        # Abre uma conexão com o banco de dados
        conexao = Database.connect()

        # Cria o cursor para executar comandos SQL
        # dictionary=True permite acessar os resultados pelo nome da coluna
        cursor = conexao.cursor(dictionary=True)

        try:
            # Busca todas as notificações
            # ORDER BY data_hora DESC coloca as mais recentes primeiro
            cursor.execute(
                "SELECT * FROM notificacao ORDER BY data_hora DESC;"
            )

            # Retorna todas as notificações encontradas
            return cursor.fetchall()

        finally:
            # Fecha o cursor depois de terminar a consulta
            cursor.close()

            # Fecha a conexão com o banco
            conexao.close()


    @classmethod
    def deletar(cls, id_notificacao):
        # Abre uma conexão com o banco de dados
        conexao = Database.connect()

        # Cria o cursor para executar o SQL
        cursor = conexao.cursor()

        try:
            # Apaga a notificação que possui o ID recebido
            cursor.execute(
                "DELETE FROM notificacao WHERE id_notificacao = %s;",
                (id_notificacao,)
            )

            # Confirma a exclusão no banco
            conexao.commit()

        finally:
            # Fecha o cursor
            cursor.close()

            # Fecha a conexão com o banco
            conexao.close()


    @classmethod
    def deletar_todas(cls):
        # Abre uma conexão com o banco de dados
        conexao = Database.connect()

        # Cria o cursor para executar comandos SQL
        cursor = conexao.cursor()

        try:
            # Apaga todas as notificações da tabela
            cursor.execute("DELETE FROM notificacao;")

            # Confirma a exclusão no banco
            conexao.commit()

        finally:
            # Fecha o cursor
            cursor.close()

            # Fecha a conexão com o banco
            conexao.close()