from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


class Funcionario(CrudBase):
    table='funcionario'
    fields=[
        'funcionario_nome',
        'funcionario_senha',
        'funcionario_cpf',
        'funcionario_cep',
        'funcionario_email',
        'funcionario_ddi',
        'funcionario_ddd',
        'funcionario_telefone',
        'funcionario_cargo'
    ]

    def __init__(self, funcionario_nome, funcionario_senha, funcionario_cpf, funcionario_cep, funcionario_email, funcionario_ddi, funcionario_ddd, funcionario_telefone, funcionario_cargo):
        self.funcionario_nome = funcionario_nome
        self.funcionario_senha = funcionario_senha
        self.funcionario_cpf = funcionario_cpf
        self.funcionario_cep = funcionario_cep
        self.funcionario_email = funcionario_email
        self.funcionario_ddi = funcionario_ddi
        self.funcionario_ddd = funcionario_ddd
        self.funcionario_telefone = funcionario_telefone
        self.funcionario_cargo = funcionario_cargo
    
    def validate(self):
        erros = [
            Validator.validar_nome(self.funcionario_nome, "nome"),
            
            Validator.validar_ddi_ddd(self.funcionario_ddi, "ddi"),
            Validator.validar_ddi_ddd(self.funcionario_ddd, "ddd"),
            Validator.validar_telefone(self.funcionario_telefone, "telefone")
        ]
        return [erro for erro in erros if erro]
        