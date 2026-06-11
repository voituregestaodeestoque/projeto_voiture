from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database

class Uso_empilhadeira(CrudBase):

    table = "uso_empilhadeira"

    fields = [
        "uso_empilhadeira_datahora",
        "funcionario_id",
        "empilhadeira_id"
    ]

    def __init__(self, uso_empilhadeira_datahora, funcionario_id, empilhadeira_id):
        self.uso_empilhadeira_datahora = datetime.now()
        self.funcionario_id = funcionario_id
        self.empilhadeira_id = empilhadeira_id

    @staticmethod
    def desocupar(id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            print("ID recebido:", id)

            sql = """
                UPDATE uso_empilhadeira
                SET funcionario_id = NULL
                WHERE id = %s
            """

            cursor.execute(sql, (id,))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def deletando(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "DELETE FROM uso_empilhadeira WHERE empilhadeira_id = %s",
                (id,)
            )

            cursor.execute(
                "DELETE FROM empilhadeira WHERE id = %s",
                (id,)
            )

            conexao.commit()

        finally:
            cursor.close()
            conexao.close()