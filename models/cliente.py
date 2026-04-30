from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


class cliente(CrudBase):
    table='cliente'
    fields=[
        'cliente_nome',
        'cliente_cpf',
        'cliente_cep',
        'cliente_email',
        'cliente_ddi',
        'cliente_ddd',
        'cliente_telefone',
        'cliente_cargo'
    ]

    def __init__(self, cliente_nome, cliente_cnpj, cliente_cep, cliente_email, cliente_ddi, cliente_ddd, cliente_telefone, cliente_descricao):
        self.cliente_nome = cliente_nome
        self.cliente_cnpj = cliente_cnpj
        self.cliente_cep = cliente_cep
        self.cliente_email = cliente_email
        self.cliente_ddi = cliente_ddi
        self.cliente_ddd = cliente_ddd
        self.cliente_telefone = cliente_telefone
        self.cliente_descricao = cliente_descricao
    
    def validate(self):
        erros = [
            Validator.validar_nome(self.cliente_nome, "nome"),
            
            Validator.validar_ddi_ddd(self.cliente_ddi, "ddi"),
            Validator.validar_ddi_ddd(self.cliete_ddd, "ddd"),
            Validator.validar_telefone(self.cliente_telefone, "telefone")
        ]
        return [erro for erro in erros if erro]