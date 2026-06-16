
#Editado por Júlia em 14/05/2026 às 11h34

from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


#-----> Classe: Fornecedor

class Fornecedor(CrudBase):
    #Definição da tabela e campos
    table='fornecedor'
    fields=[
        'fornecedor_nome',
        'fornecedor_cnpj',
        'fornecedor_cep',
        'fornecedor_email',
        'fornecedor_ddi',
        'fornecedor_ddd',
        'fornecedor_telefone',
        'fornecedor_descricao'
    ]


    #Definição dos valores para cada campo
    def __init__(self, fornecedor_nome,fornecedor_cnpj,fornecedor_cep,fornecedor_email,fornecedor_ddi,fornecedor_ddd,fornecedor_telefone,fornecedor_descricao):
        self.fornecedor_nome = fornecedor_nome
        self.fornecedor_cnpj = fornecedor_cnpj
        self.fornecedor_cep = fornecedor_cep
        self.fornecedor_email = fornecedor_email
        self.fornecedor_ddi = fornecedor_ddi
        self.fornecedor_ddd = fornecedor_ddd
        self.fornecedor_telefone = fornecedor_telefone
        self.fornecedor_descricao = fornecedor_descricao


######################################################################################
#---> Início: Validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            #nome 
            Validator.validar_nome(self.fornecedor_nome, "fornecedor_nome"),
            #cnpj válido
            Validator.validar_cpf_cnpj(self.fornecedor_cnpj, "fornecedor_cnpj"),
            #cep 
            Validator.validar_cep(self.fornecedor_cep, "fornecedor_cep"),
            #email válido
            Validator.validar_email(self.fornecedor_email, "fornecedor_email"),
            #ddi
            Validator.validar_ddi_ddd(self.fornecedor_ddi, "fornecedor_ddi"),
            #ddd
            Validator.validar_ddi_ddd(self.fornecedor_ddd, "fornecedor_ddd"),
            #telefone
            Validator.validar_telefone(self.fornecedor_telefone, "fornecedor_telefone")
        ]
        
        #Passa em cada item da lista com os retornos das validações
        for item in validacoes:
            #Verifica se não o retorno não é vazio e o retorno é Falso
            if item is not None and not item['valida']:
                #adiciona em uma lista todas as mensagens de erro vindas das validações
                erros.append(item["mensagem"])

        #Retorna a lista com todas as mensagens de erro
        return erros

#---> Fim: Validar os campos da tabela
######################################################################################

    
######################################################################################
#---> Início: Listar todos os fornecedores registrados

    #Define um método da classe
    @classmethod

    #Define uma função
    def listagem(cls):

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de selecionar
        try:
            #Define o comando SQL que buscará todos os fornecedores
            sql = "SELECT * FROM fornecedor"

            #Executa o comando
            cursor.execute(sql)

            #Retorna a listagem de todos os fornecedores
            return cursor.fetchall()
        
        #Encerra a função
        finally:

            #Fecha o cursor
            cursor.close()

            #Encerra a conexão com o banco de dados
            conexao.close()

#---> Fim: Listar todos os fornecedores registrados
######################################################################################


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
            #Monta uma lista que conta quantas vezes fornecedor apararece na tabela de pedido de entrada
            queries = [

                #Comando SQL para a contagem
                "SELECT COUNT(*) FROM pedido_entrada WHERE fornecedor_id = %s"
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


######################################################################################
#---> Início: Deletar com segurança

    #Define um método da classe
    @classmethod

    #Define uma função
    def safe_delete(cls, id):

        #Seleciona o ID do fornecedor
        fornecedor = cls.find_by_id(id)

        #Caso não haja fornecedor com aquele ID
        if not fornecedor:

            #Interrompe a execução e apresenta uma mensagem de erro
            raise ValueError("Fornecedor não encontrado.")

        #Verifica se aquele fornecedor tem conexão com outra tabela
        if cls.has_related_records(id):

            #Interrompe a execução e apresenta uma mensagem de erro
            raise ValueError("Não é possível excluir o fornecedor porque ele está vinculado a outros serviços.")
        
        #Exclui o fornecedor
        cls.delete(id)

#---> Fim: Deletar com segurança
######################################################################################


######################################################################################   
#---> Início: Busca por CNPJ já cadastrado

    #Define um método da classe
    @classmethod

    #Define uma função
    def cnpj_existente(cls, cnpj):

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True, buffered=True) #buffered para armazenar os resultados em memória, evitando erros ao fazer mais consultas

        #Inicia uma tentativa de selecionar na tabela fornecedores com o CNPJ digitado
        try:

            #Define o comando SQL que procurará esse fornecedor
            sql = f"SELECT * FROM {cls.table} WHERE fornecedor_cnpj = %s"

            #Executa o comando com o CNPJ digitado
            cursor.execute(sql, (cnpj,))

            #Retorna a seleção do fornecedor com aquele CNPJ
            return cursor.fetchone()
        
        #Encerra a execução
        finally:

            #Fecha o cursor
            cursor.close()

            #Encerra a conexão
            conexao.close()

#---> Fim: Busca por CNPJ já cadastrado
######################################################################################
   

######################################################################################
#---> Início: Busca por email já cadastrado

    #Define um método da classe
    @classmethod

    #Define uma função
    def email_existente(cls, email):

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True, buffered=True) #buffered para armazenar os resultados em memória, evitando erros ao fazer mais consultas

        #Inicia uma tentativa de selecionar na tabela fornecedores com o email digitado
        try:

            #Define o comando SQL que procurará esse fornecedor
            sql = f"SELECT * FROM {cls.table} WHERE fornecedor_email = %s"

            #Executa o comando com o CNPJ digitado
            cursor.execute(sql, (email,))

            #Retorna a seleção do fornecedor com aquele CNPJ
            return cursor.fetchone()
        
        #Encerra a execução
        finally:

            #Fecha o cursor
            cursor.close()

            #Encerra a conexão
            conexao.close()

#---> Fim: Busca por CNPJ já cadastrado
######################################################################################