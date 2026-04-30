from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


class Fornecedor(CrudBase):
    table='fornecedor'
    fields=[
        'fornecedor_nome',
        'fornecedor_cnpj',
        'fornecedor_cep',
        'fornecedor_email',
        'fornecedor_ddi',
        'fornecedor_ddd',
        'fornecedor_telefone',
        'fornecedor_descricao'
    ]

    def __init__(self, fornecedor_nome,fornecedor_cnpj,fornecedor_cep,fornecedor_email,fornecedor_ddi,fornecedor_ddd,fornecedor_telefone,fornecedor_descricao):
        self.fornecedor_nome = fornecedor_nome
        self.fornecedor_cnpj = fornecedor_cnpj
        self.fornecedor_cep = fornecedor_cep
        self.fornecedor_email = fornecedor_email
        self.fornecedor_ddi = fornecedor_ddi
        self.fornecedor_ddd = fornecedor_ddd
        self.fornecedor_telefone = fornecedor_telefone
        self.fornecedor_descricao = fornecedor_descricao

    def validate(self):
        erros = []
        nome = Validator.validar_nome(self.fornecedor_nome, "fornecedor_nome")
        if not nome["valida"]:
            erros.append(nome["mensagem"])
        return erros