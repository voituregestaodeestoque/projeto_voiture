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
