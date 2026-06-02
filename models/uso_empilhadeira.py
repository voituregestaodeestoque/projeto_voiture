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

        print("ID recebido:", id)

        sql = """
            UPDATE uso_empilhadeira
            SET funcionario_id = NULL
            WHERE id = %s
        """

        cursor.execute(sql, (id,))
        print("Linhas afetadas:", cursor.rowcount)

        conexao.commit()

        cursor.close()
        conexao.close()