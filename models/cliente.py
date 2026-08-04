#faz todas as importações que iremos utilizar na classe cliente
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

#atualizado por Ryan dia 04/06/2026 às 17:10

class Cliente(CrudBase):#cria a classe Cliente
    table='cliente'#nome da tabela
    fields=[
        'cliente_nome',
        'cliente_cnpj',
        'cliente_cep',
        'cliente_email',
        'cliente_ddi',
        'cliente_ddd',
        'cliente_telefone',
        'cliente_descricao'
    ]
    #campos que existem na tabela


    # metodo que cria um objeto 
    #o self passa os dados de cada campo
    def __init__(self, cliente_nome, cliente_cnpj, cliente_cep, cliente_email, cliente_ddi, cliente_ddd, cliente_telefone, cliente_descricao):
        self.cliente_nome = cliente_nome
        self.cliente_cnpj = cliente_cnpj
        self.cliente_cep = cliente_cep
        self.cliente_email = cliente_email
        self.cliente_ddi = cliente_ddi
        self.cliente_ddd = cliente_ddd
        self.cliente_telefone = cliente_telefone
        self.cliente_descricao = cliente_descricao
    
    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            #nome
            Validator.validar_nome(self.cliente_nome, "cliente_nome"),
            #cnpj
            Validator.validar_cnpj(self.cliente_cnpj, "cliente_cnpj"),
            #cep
            Validator.validar_cep(self.cliente_cep, "cliente_cep"),
            #email
            Validator.validar_email(self.cliente_email, "cliente_email"),
            #ddi
            Validator.validar_ddi_ddd(self.cliente_ddi, "cliente_ddi"),
            #ddd
            Validator.validar_ddi_ddd(self.cliente_ddd, "cliente_ddd"),
            #telefone
            Validator.validar_telefone(self.cliente_telefone, "cliente_telefone"),
            #decrição
            Validator.validar_descricao(self.cliente_descricao, "cliente_descricao")
        ]

        #Passa em cada item da lista com os retornos das validações
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros
    #função para listar os clientes registrados
    @classmethod
    #Define uma função
    def cliente_listagem(cls):
        #Conecta com o banco de dados
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            #Define o comando SQL que buscará todos os fornecedores
            sql = "SELECT * FROM cliente"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    #Função para deletar com segurança
    @classmethod
    #Define uma função
    def safe_delete(cls, id):
        fornecedor = cls.find_by_id(id)
        if not fornecedor:
            raise ValueError("Cliente não encontrado.")

        if cls.has_related_records(id):

            #Interrompe a execução e apresenta uma mensagem de erro
            raise ValueError("Não é possível excluir o cliente porque ele está vinculado a outros serviços.")
        cls.delete(id)

    #Procura no banco algum cliente com o mesmo CNPJ
    @classmethod
    #Define uma função
    def cnpj_existente(cls, cnpj):
        #Conecta com o banco de dados
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True, buffered=True)
        try:
            #Define o comando SQL que buscará todos os fornecedores
            sql = f"SELECT * FROM {cls.table} WHERE cliente_cnpj = %s"
            cursor.execute(sql, (cnpj,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()
    
    #Procura no banco algum cliente com o mesmo email
    @classmethod
    #Define uma função
    def email_existente(cls, email):
        #Conecta com o banco de dados
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True, buffered=True)
        try:
            #Define o comando SQL que buscará todos os fornecedores
            sql = f"SELECT * FROM {cls.table} WHERE cliente_email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone()
            #Enecerra a execução
        finally:
            cursor.close()
            conexao.close()


######################################################################################
#---> Início: Busca por tabela relacionada

    #Define um método da classe
    @classmethod

    #define uma função
    def has_related_records(cls, id):

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor()

        #Inicia uma tentativa
        try:
            #Monta uma lista que conta quantas vezes cliente aparece na tabela de pedido de entrada
            queries = [

                #Comando SQL para a contagem
                "SELECT COUNT(*) FROM pedido_saida WHERE cliente_id = %s"
            ]
            #Define a quantidade inicial como zero
            total = 0

            #executará cada comando da lista de comandos
            for sql in queries:

                #executa o comando SQL
                cursor.execute(sql, (id,))

                #Soma a contagem do SQL à quantidade inicial
                total += cursor.fetchone()[0]

            #Retorna a soma maior que zero
            return total > 0
        
        #Enecerra a execução
        finally:

            #Fecha o cursor
            cursor.close()

            #Encerra a conexão
            conexao.close()

#---> Fim: Busca por tabela relacionada
######################################################################################
