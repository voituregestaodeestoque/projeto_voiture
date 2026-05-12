from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

#atualizado por Ryan dia 12/05/2026 às 10:10

class Cliente(CrudBase):
    table='cliente'
    fields=[
        'cliente_nome',
        'cliente_cnpj',
        'cliente_cep',
        'cliente_email',
        'cliente_ddi',
        'cliente_ddd',
        'cliente_telefone',
        'cliente_descricao'
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
    
    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            Validator.validar_nome(self.cliente_nome, "cliente_nome"),
            Validator.validar_cpf_cnpj(self.cliente_cnpj, "cliente_cnpj"),
            Validator.validar_cep(self.cliente_cep, "cliente_cep"),
            Validator.validar_email(self.cliente_email, "cliente_email"),
            Validator.validar_ddi_ddd(self.cliente_ddi, "cliente_ddi"),
            Validator.validar_ddi_ddd(self.cliente_ddd, "cliente_ddd"),
            Validator.validar_telefone(self.cliente_telefone, "cliente_telefone"),
            Validator.validar_descricao(self.cliente_descricao, "cliente_descricao")
        ]
        
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def cliente_listagem(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM cliente"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    #Função para deletar com segurança
    @classmethod
    def safe_delete(cls, id):
        fornecedor = cls.find_by_id(id)
        if not fornecedor:
            raise ValueError("Cliente não encontrado.")
        cls.delete(id)

