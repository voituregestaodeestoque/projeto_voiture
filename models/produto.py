# Editado por Júlia em 26/05/2026 às 11h18

from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Produto(CrudBase):
    table = "produto"
    fields = [
        'produto_nome',
        'produto_descricao', 
        'produto_categoria',
        'produto_quantidade_minima',
        'produto_preco_custo', 
        'produto_preco_venda',
        'produto_peso',
        'produto_localizacao',
    ]

    def __init__(self, produto_nome, produto_descricao, produto_categoria, produto_quantidade_minima,
                 produto_preco_custo, produto_preco_venda, produto_peso, produto_localizacao):
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.produto_quantidade_minima = produto_quantidade_minima
        self.produto_preco_custo = produto_preco_custo
        self.produto_preco_venda = produto_preco_venda
        self.produto_peso = produto_peso
        self.produto_localizacao = produto_localizacao


    def validate(self):
        erros = []

        validacoes = [
            Validator.required(self.produto_nome, "produto_nome"),
            Validator.validar_quantidade(self.produto_quantidade_minima, "produto_quantidade_minima"),
            Validator.validar_preco(self.produto_preco_custo, "produto_preco_custo"),
            Validator.validar_preco(self.produto_preco_venda, "produto_preco_venda"),
            Validator.validar_peso(self.produto_peso, "produto_peso"),
            Validator.validar_localizacao(self.produto_localizacao, "produto_localizacao")
        ]
        
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def produto_listagem(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def safe_delete(cls, id):
        produto = cls.find_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o produto porque ele está vinculado a outros serviços.")
        cls.delete(id)

    
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM pedido_entrada WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_saida WHERE produto_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()




    @classmethod
    def produto_total(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT COUNT(produto_nome) as quantidade_produto FROM produto"
            cursor.execute(sql)
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()