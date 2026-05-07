from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Empilhadeira(CrudBase):
    table = "empilhadeira"
    fields = [
        "empilhadeira_chassi",
        "empilhadeira_status",
        "empilhadeira_modelo",
        "empilhadeira_marca"]

    def __init__(self, empilhadeira_chassi, empilhadeira_status="PENDENTE", empilhadeira_modelo="", empilhadeira_marca=""):
        self.empilhadeira_chassi = empilhadeira_chassi
        self.empilhadeira_status = empilhadeira_status
        self.empilhadeira_modelo = empilhadeira_modelo
        self.empilhadeira_marca = empilhadeira_marca

    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            Validator.validar_chassi(self.empilhadeira_chassi, "empilhadeira_chassi"),
            Validator.validar_modelo(self.empilhadeira_modelo, "empilhadeira_modelo"),
            Validator.validar_marca(self.empilhadeira_marca, "empilhadeira_marca")
        ]
        
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def tabelatudojunto(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "select u.*, f.funcionario_nome, e.* from uso_empilhadeira as u inner join funcionario as f on u.funcionario_id = f.id inner join empilhadeira as e on u.empilhadeira_id= e.id ;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def empilhadeirasemuso(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT e.* FROM empilhadeira as e LEFT JOIN uso_empilhadeira as u ON e.id = u.empilhadeira_id WHERE u.empilhadeira_id IS NULL;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    #Função para deletar com segurança
    @classmethod
    def safe_delete(cls, id):
        print('delete', cls,id)
        empilhadeira = cls.find_by_id(id)
        if not empilhadeira:
            raise ValueError("Empilhadeira não encontrada.")
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir a empilhadeira porque ele está vinculado a outros serviços.")
        cls.delete(id)

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM pedido_entrada WHERE empilhadeira_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()


