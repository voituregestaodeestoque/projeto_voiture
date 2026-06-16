#Editado por Júlia em 02/06/2026 as 16h46

from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


#-----> Classe: Estoque

class Estoque(CrudBase):
    #Definição da tabela e campos
    table = "estoque"
    fields = [
        "estoque_quantidade",
        "produto_id"]

    #Definição dos valores para cada campo
    def __init__(self, estoque_quantidade, produto_id=0):
        self.estoque_quantidade = estoque_quantidade
        self.produto_id = produto_id


    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            #quantidade
            Validator.validar_quantidade(self.estoque_quantidade, "estoque_quantidade")
        ]
        
        #Passa em cada item da lista com os retornos das validações
        for itens in validacoes:
            #Verifica se o retorno é Falso
            if not itens['valida']:
                #adiciona em uma lista todas as mensagens de erro vindas das validações
                erros.append(itens["mensagem"])

        #Retorna a lista com todas as mensagens de erro
        return erros


######################################################################################
#---> Início: Deletar produto e estoque

    @classmethod #Define um método da classe

    def delete_by_produto(cls, id): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor()

        #Inicia uma tentativa de deletar
        try:
            sql = "DELETE FROM estoque WHERE produto_id = %s" #Define o comando SQL que excluirá o estoque
            cursor.execute(sql, (id,)) #Executa o comando
            conexao.commit() #Atualiza
            return cursor.rowcount #Retorna a nova contagem de linhas 

        except Exception: #Erro
            conexao.rollback() #Retorna o processo
            raise #Limpa as alterações

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

#---> Fim: Deletar produto e estoque
######################################################################################


######################################################################################
#---> Início: Listagem de estoque

    @classmethod #Define um método da classe
    def card_estoque(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by p.id DESC" 

            cursor.execute(sql) #Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos em estoque

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

#---> Fim: Listagem de estoque
######################################################################################


######################################################################################
#---> Início: Filtros de ordenação

    @classmethod #Define um método da classe
    def card_estoque_nome(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by produto_nome ASC"

            cursor.execute(sql)#Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão
    
    @classmethod #Define um método da classe
    def card_estoque_maior(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by estoque_quantidade DESC"

            cursor.execute(sql) #Executa o comando
            return cursor.fetchall()#Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

    @classmethod #Define um método da classe
    def card_estoque_menor(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by estoque_quantidade ASC"

            cursor.execute(sql) #Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

    @classmethod #Define um método da classe
    def card_estoque_preco_maior(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by produto_preco_venda DESC"

            cursor.execute(sql) #Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão
    
    @classmethod #Define um método da classe
    def card_estoque_preco_menor(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by produto_preco_venda ASC"

            cursor.execute(sql) #Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão


#---> Fim: Filtros de ordenação
######################################################################################


######################################################################################
#---> Início: Produtos com estoque baixo

    @classmethod #Define um método da classe
    def estoque_baixo(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT e.estoque_quantidade,p.produto_nome,p.produto_quantidade_minima FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id WHERE e.estoque_quantidade <= p.produto_quantidade_minima * 1.1;"

            cursor.execute(sql) #Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

#---> Fim: Produtos com estoque baixo
######################################################################################


######################################################################################
#---> Início: Soma dos estoques de todos os produtos

    @classmethod #Define um método da classe
    def estoque_total(cls): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Define o comando SQL que fará a seleção dos produtos
            sql = "SELECT SUM(estoque_quantidade) as quantidade_total FROM estoque"

            cursor.execute(sql) #Executa o comando
            return cursor.fetchone() #Retorna a seleção dos produtos

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

#---> Fim: Soma dos estoques de todos os produtos
######################################################################################


######################################################################################
#---> Início: Pesquisa de produtos


    @classmethod #Define um método da classe
    def card_estoque_pesquisa(cls, chave_pesquisa): #Define uma função

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor(dictionary=True)

        #Inicia uma tentativa de listar
        try:
            #Monta uma busca com a chave de pesquisa
            busca = f"%{chave_pesquisa['chave_pesquisa']}%"

            #Define o comando SQL que fará a seleção dos produtos
            sql = f"SELECT e.estoque_quantidade, p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id WHERE p.produto_nome LIKE %s order by p.id"

            cursor.execute(sql, (busca,)) #Executa o comando
            return cursor.fetchall() #Retorna a seleção dos produtos
        
        except Exception as e: #Erro
            raise #Limpa

        finally:
            cursor.close() #Fecha o cursor
            conexao.close() #Encerra a conexão

#---> Fim: Pesquisa de produtos
######################################################################################