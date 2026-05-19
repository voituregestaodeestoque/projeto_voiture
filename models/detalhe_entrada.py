from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_entrada import Pedido_entrada

class Detalhe_entrada(CrudBase):
    table = "detalhe_entrada"
    fields = [
        'detalhe_entrada_quantidade'
    ]

    def __init__(self, detalhe_entrada_quantidade):
        self.detalhe_entrada_quantidade = detalhe_entrada_quantidade

    
    @classmethod
    def pedido_entrada_join(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "select f.fornecedor_nome, d.detalhe_entrada_quantidade, p.* from pedido_entrada as p inner join fornecedor as f on p.fornecedor_id = p.fornecedor_id inner join detalhe_entrada as d;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
