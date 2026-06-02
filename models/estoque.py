#Editado por Júlia em 26/05/2026 às 11h01
from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Estoque(CrudBase):
    table = "estoque"
    fields = [
        "estoque_quantidade",
        "produto_id"]

    def __init__(self, estoque_quantidade, produto_id=0):
        self.estoque_quantidade = estoque_quantidade
        self.produto_id = produto_id

    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            Validator.validar_quantidade(self.estoque_quantidade, "estoque_quantidade")
        ]
        
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def card_estoque(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by p.id DESC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def card_estoque_nome(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by produto_nome ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    
    @classmethod
    def card_estoque_maior(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by estoque_quantidade DESC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def card_estoque_menor(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by estoque_quantidade ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def card_estoque_preco_maior(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by produto_preco_venda DESC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    
    @classmethod
    def card_estoque_preco_menor(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.* FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id order by produto_preco_venda ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def estoque_baixo(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.estoque_quantidade,p.produto_nome,p.produto_quantidade_minima FROM estoque AS e INNER JOIN produto AS p ON p.id = e.produto_id WHERE e.estoque_quantidade <= p.produto_quantidade_minima * 1.1;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def estoque_total(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT SUM(estoque_quantidade) as quantidade_total FROM estoque"
            cursor.execute(sql)
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def encontrar_produto(cls, produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(
            "SELECT * FROM estoque WHERE produto_id = %s",
            (produto_id,)
        )

            return cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

    

    