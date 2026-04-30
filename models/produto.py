from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Produto(CrudBase):
    table = "Produto"
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


"""
    def validate(self):
        erros = [
            Validator.required(self.produto_nome, "nome"),
            Validator.non_negative(self.produto_quantidade_minima, "quantidade minima"),
            Validator.non_negative(self.produto_preco_custo, "preço de custo"),
            Validator.non_negative(self.produto_preco_venda, "preço de venda")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def low_stock(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto WHERE quantidade <= estoque_minimo ORDER BY nome"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def update_quantity(cls, id, nova_quantidade, connection=None):
        conexao = connection or Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE produto SET quantidade = %s WHERE id = %s"
            cursor.execute(sql, (nova_quantidade, id))
            if connection is None:
                conexao.commit()
            return cursor.rowcount
        except Exception:
            if connection is None:
                conexao.rollback()
            raise
        finally:
            cursor.close()
            if connection is None:
                conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_movimentacao WHERE produto_id = %s"
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
    def safe_delete(cls, id):
        produto = cls.find_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.")
        cls.delete(id)"""