#importações usadas na classe pedido_entrada
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from datetime import datetime

#classe pedido_entrada
class Pedido_entrada(CrudBase):
    table = "pedido_entrada"
    fields = [
        'status_pedido_entrada', 
        'fornecedor_id',
        'data_pedido_entrada'
    ]

    #define os valores para cada campo
    def __init__(self, status_pedido_entrada, fornecedor_id, data_pedido_entrada):
        self.status_pedido_entrada = status_pedido_entrada
        self.fornecedor_id = fornecedor_id
        self.data_pedido_entrada = data_pedido_entrada

    #método para coletar informações de quatro tabelas
    @classmethod
    #função que reúne informações de quatro tabelas: fornecedor, detalhe_entrada, movimentacao_entrada e pedido_entrada
    def pedido_entrada_join(cls):
        conexao = Database.connect() #conexão com o banco
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario
        #código sql para reunir as informações específicas
        try:
            sql = """select f.fornecedor_nome, d.detalhe_entrada_quantidade, d.detalhe_entrada_item, me.datahora_movimentacao_entrada, p.* from pedido_entrada as p 
            INNER JOIN fornecedor as f 
            ON p.fornecedor_id = f.id 
            INNER JOIN detalhe_entrada d 
            ON p.id = d.pedido_entrada_id
            INNER JOIN movimentacao_entrada me
            ON p.id = me.detalhe_entrada_pedido_entrada_id;"""
            cursor.execute(sql) #executa consulta sql
            return cursor.fetchall() #retorna todos os registros encontrados
        finally:#encerra cursor e a conexão com o banco
            cursor.close()
            conexao.close()


    #função de validação
    def validate(self):
        erros = []

        #valida os campos
        validacoes = [
            Validator.required(self.status_pedido_entrada, "status_pedido_entrada"),
            Validator.required(self.fornecedor_id, "fornecedor_id")
        ]

        for itens in validacoes:
            if not itens['valida']: #verifica se o retorno é False
                erros.append(itens["mensagem"]) #adiciona em uma lista todas as mensagens de erro

        return erros

    #método para buscar pedidos de entrada
    @classmethod
    #função que busca pedidos de entrada e organiza os pedidos dos mais recentes para os mais antigos
    def find_all_ordered(cls):
        conexao = Database.connect() #conexão com o banco
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario
        #SELECT: seleciona as tabelas que serão utilizadas
        #LEFT JOIN: relaciona diferentes tabelas
        #GROUP BY: agrupa os registros pelas colunas indicadas
        #ORDER BY: ordena os pedidos pelo id em ordem decrescente
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
                    
            cursor.execute(sql) #executa sql
            return cursor.fetchall() #retorna todos os registros
        finally: #encerra cursor e conexão com o banco
            cursor.close()
            conexao.close()

    #método para finalizar um pedido de entrada
    @classmethod
    #função que atualiza a quantidade de produtos de um pedido de entrada
    def finalizar(cls, pedido_entrada_id):
        conexao = Database.connect() #conexão com banco de dados
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario

        try:
            #inicia uma transação no banco, ou seja, agrupa operações para que possam ser confirmadas ou desfeitas
            conexao.start_transaction()
            #executa comando sql
            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s", (pedido_entrada_id,))
            pedido = cursor.fetchone() #retorna uma única linha(um registro)

            #se não encontrar o pedido
            if not pedido:
                conexao.rollback()
                return "Pedido não encontrado."

            #se o status do pedido não for pendente
            if pedido["status_pedido_entrada"] != "PENDENTE":
                conexao.rollback()
                return "Somente pedidos abertos podem ser finalizados."
            #executa comando sql
            cursor.execute(
                "SELECT * FROM detalhe_entrada WHERE pedido_entrada_id = %s",
                (pedido_entrada_id,)
            )
            itens = cursor.fetchall() #retorna uma lista com os itens encontrados

            #se o pedido não tiver nenhum item, verifica se tem pelo menos um item
            if not itens:
                conexao.rollback()
                return "Não é possível finalizar um pedido sem itens."

            #percorre por todos os itens de um pedido para atualizar seu estoque
            for item in itens:
                #executa comando sql
                #busca o estoque do produto
                cursor.execute(
                """
                SELECT *
                FROM estoque
                WHERE produto_id = %s
                """,
                (item["produto_id"],))

                estoque = cursor.fetchone() #retorna um registro
                if not estoque:#se não encontrar o registro de estoque do produto
                    conexao.rollback()
                    return "Produto não encontrado no pedido."

                #cálculo da nova quantidade
                nova_quantidade = estoque["estoque_quantidade"] + item["detalhe_entrada_quantidade"]

                #executa comando sql de atualziar
                cursor.execute(
                """ 
                    UPDATE estoque
                    SET estoque_quantidade = %s
                    WHERE produto_id = %s
                    """,
                    (nova_quantidade, item["produto_id"]) )
                
            conexao.commit() #confirma alterações feitas do banco de dados
            return "Pedido de entrada atualizado com sucesso."

        except Exception: #exceções do try
            conexao.rollback() #desfaz alterações não confirmadas pela transação
            return "Erro ao atualizar pedido de entrada."
        finally:
            cursor.close()
            conexao.close()

    #método que busca um pedido de entrada pelo id
    @classmethod
    def find_by_id(cls, pedido_entrada_id):
        conexao = Database.connect() #conexão com o banco de dados
        cursor = conexao.cursor(dictionary=True)

        #seleciona dados, relaciona com a tabela fornecedor
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
            cursor.execute(sql, (pedido_entrada_id,))#executa comando sql
            return cursor.fetchone() #retorna um único registro
        finally:
            cursor.close()
            conexao.close()

    #método de processar pedido de entrada    
    @classmethod
    def processar(cls, pedido_entrada_id):
        conexao = Database.connect() #conexão com o banco de dados
        cursor = conexao.cursor(dictionary=True)
        try:
            #inicia uma transação no banco, ou seja, agrupa operações para que possam ser confirmadas ou desfeitas
            conexao.start_transaction()
            #executa comando sql
            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s FOR UPDATE", (pedido_entrada_id,))
            pedido = cursor.fetchone()#retorna um único registro
            if not pedido: #se não encontrar pedido
                raise ValueError("Pedido de entrada não encontrado.")
            #se o status for diferente de pendente
            if pedido["status_pedido_entrada"] != "PENDENTE":
                raise ValueError("Somente pedidos pendentes podem ser processados.")
            #executa comando sql
            cursor.execute("SELECT * FROM detalhe_entrada WHERE pedido_entrada_id = %s FOR UPDATE", (pedido_entrada_id,))

            detalhes = cursor.fetchall() #retorna todos os registros encontrados

            if not detalhes: #impede que um pedido sem itens seja processado
                raise ValueError("Pedido sem itens.")
            
            #percorre cada item do pedido
            for detalhe in detalhes:
                cursor.execute( #executa comando sql
                    """
                    SELECT *
                    FROM estoque
                    WHERE produto_id = %s
                    FOR UPDATE
                    """,
                    (detalhe["produto_id"],)
                )
                estoque = cursor.fetchone() #retorna um unico registro

                if not estoque: #se não encontrar registro de estoque do produto
                    raise ValueError(
                        f"Não existe estoque para o produto {detalhe['produto_id']}"
                    )

                #cálcula para a nova quantidade
                nova_quantidade = (
                    estoque["estoque_quantidade"]
                    + detalhe["detalhe_entrada_quantidade"]
                )                
                
                #executa comando sql de atualização de estoque
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

                #executa comando sql para inserir informação de data do processamento na tabela movimentacao_entrada
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

            #executa comando sql para atualização do status do pedido de entrada
            cursor.execute(
                """
                UPDATE pedido_entrada
                SET status_pedido_entrada = %s
                WHERE id = %s
                """,
                ("CONCLUIDO", pedido_entrada_id,)
            )
            
            conexao.commit() #confirma alterações feitas do banco de dados
            return "Pedido de entrada processado com sucesso."
        finally:
            cursor.close()
            conexao.close()

    #método para cancelar pedido de entrada
    @classmethod
    def cancelar(cls, pedido_entrada_id):
        conexao = Database.connect()#conexão com o banco de dados
        cursor = conexao.cursor(dictionary=True)
        try:
            #executa comando sql
            cursor.execute("SELECT * FROM pedido_entrada WHERE id = %s", (pedido_entrada_id,))
            pedido = cursor.fetchone() #retorna um único registro
            if not pedido: #se não encontrar pedido
                raise ValueError("Pedido de entrada não encontrado.")
            if pedido["status_pedido_entrada"] != "PENDENTE": #se o status do pedido for diferente de pendente
                raise ValueError("Somente pedidos pendentes podem ser cancelados.")

            cursor = conexao.cursor()#cria cursor para executar atualização
            cursor.execute( #executa comando sql de atualização de status de pedido de entrada
                """
                UPDATE pedido_entrada
                SET status_pedido_entrada = %s
                WHERE id = %s
                """,
                ("CANCELADO", pedido_entrada_id,)
            )
            conexao.commit() #confirma alterações feitas do banco de dados
            return "Pedido de entrada cancelado com sucesso."
        except Exception:#exceções do try
            conexao.rollback() #desfaz alterações não confirmadas pela transação
            raise #lançar execução
        finally:
            cursor.close()
            conexao.close()

    #método para verificar pedidos de entrada pendentes
    @classmethod
    #função que  busca pedidos de entrada pendentes
    def pedidoentrada_pendente(cls):
        conexao = Database.connect() #conexão com o banco de dados
        cursor = conexao.cursor(dictionary=True)
        try:
            #executa comando sql
            sql = "SELECT * FROM pedido_entrada WHERE status_pedido_entrada = 'pendente';"
            cursor.execute(sql)
            return cursor.fetchall() #retorna todos os registros
        finally:
            cursor.close()
            conexao.close()

    #método para contar a quantidade de pedido de entrada
    @classmethod
    #função que conta quantos pedidos de entrada estão pendentes
    def contar_pedidoentrada(cls):
        conexao = Database.connect() #conexão com o banco de dados
        cursor = conexao.cursor(dictionary=True)
        try:
            #executa comando sql para contar
            sql = "SELECT COUNT(status_pedido_entrada) as pedido_entrada_total FROM pedido_entrada WHERE status_pedido_entrada = 'pendente';"
            cursor.execute(sql)
            return cursor.fetchone() #retorna um único registro
        finally:
            cursor.close()
            conexao.close()

    #método que conta a quantidade de produtos recebidos nos pedidos      
    @classmethod
    def total_entradas(cls):
        conexao = Database.connect()#conexão com o banco de dados
        cursor = conexao.cursor(dictionary=True)

        try:
            #executa comando sql
            sql = """
                SELECT SUM(ds.detalhe_entrada_quantidade) AS total
                FROM detalhe_entrada ds
                INNER JOIN pedido_entrada ps
                    ON ds.pedido_entrada_id = ps.id
                WHERE ps.status_pedido_entrada = 'CONCLUIDO'
            """

            cursor.execute(sql)
            resultado = cursor.fetchone() # retorna um único registro

            return resultado["total"] or 0 #retorna valor da soma ou 0 caso for None

        finally:
            cursor.close()
            conexao.close()