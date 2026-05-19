# Editado por Júlia em 19/05/2026 às 12h13

from datetime import datetime
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Estoque(CrudBase):
    table = "estoque"
    fields = [
        "estoque_quantidade",
        "produto_id"]

    def __init__(self, estoque_quantidade, produto_id = 0):
        self.estoque_quantidade = estoque_quantidade
        self.produto_id = produto_id

    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            Validator.validar_quantidade(self.estoque_quantidade, "estoque_quantidade")
        ]
        
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros
