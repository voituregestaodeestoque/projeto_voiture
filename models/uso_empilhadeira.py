#faz todas as importações que iremos utilizar na classe uso_empilhadeira
from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database

class Uso_empilhadeira(CrudBase):#cria a classe Uso_empilhadeira

    table = "uso_empilhadeira"#nome da tabela

    fields = [
        "uso_empilhadeira_datahora",
        "funcionario_id",
        "empilhadeira_id"
    ]
    #campos que existem na tabela


    # metodo que cria um objeto 
    #o self passa os dados de cada campo
    def __init__(self, uso_empilhadeira_datahora, funcionario_id, empilhadeira_id):
        self.uso_empilhadeira_datahora = datetime.now()
        self.funcionario_id = funcionario_id
        self.empilhadeira_id = empilhadeira_id
