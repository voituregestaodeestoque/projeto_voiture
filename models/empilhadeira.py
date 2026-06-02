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
            sql = sql = """SELECT
    u.id AS uso_id,
    u.uso_empilhadeira_datahora,
    u.funcionario_id,
    u.empilhadeira_id,

    f.funcionario_nome,

    e.id AS empilhadeira_id_real,
    e.empilhadeira_chassi,
    e.empilhadeira_modelo,
    e.empilhadeira_marca,
    e.empilhadeira_status

FROM uso_empilhadeira u
INNER JOIN funcionario f
    ON u.funcionario_id = f.id
INNER JOIN empilhadeira e
    ON u.empilhadeira_id = e.id
WHERE u.funcionario_id IS NOT NULL
"""
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
            sql = """ SELECT e.* FROM empilhadeira e LEFT JOIN uso_empilhadeira u ON e.id = u.empilhadeira_id AND u.funcionario_id IS NOT NULL WHERE u.id IS NULL """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    #Função para deletar com segurança
    @classmethod
    def safe_delete(cls, id):
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
                "SELECT COUNT(*) FROM uso_empilhadeira WHERE empilhadeira_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()


