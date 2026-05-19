# Editado por Ryan em 19/05/2026 às 12h17


#importa as coisas do core
from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Estoque(CrudBase):
    #nome da tabela
    table = "estoque"
    #nome dos campos
    fields = [
        "estoque_quantidade",
        "produto_id"]

    #os valores da tabela
    def __init__(self, estoque_quantidade, produto_id = 0):
        self.estoque_quantidade = estoque_quantidade
        self.produto_id = produto_id

    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            #valida a quantidade de produto no estoque 
            Validator.validar_quantidade(self.estoque_quantidade, "estoque_quantidade")
        ]
        
        #faz os erros 
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        #retorna os erros
        return erros
