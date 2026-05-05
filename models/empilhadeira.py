from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database

class Empilhadeira(CrudBase):
    table = "empilhadeira"
    fields = [
        "empilhadeira_chassi",
        "empilhadeira_status",
        "empilhadeira_modelo",
        "empilhadeira_marca"]

    def __init__(self, empilhadeira_chassi, empilhadeira_status, empilhadeira_modelo, empilhadeira_marca):
        self.empilhadeira_chassi = empilhadeira_chassi
        self.empilhadeira_status = empilhadeira_status
        self.empilhadeira_modelo = empilhadeira_modelo
        self.empilhadeira_marca = empilhadeira_marca

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




