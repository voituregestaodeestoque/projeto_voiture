
#Editado por Júlia em 07/05/2026 às 12h26

from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator


#-----> Classe: Fornecedor

class Fornecedor(CrudBase):
    #Definição da tabela e campos
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


    #Definição dos valores para cada campo
    def __init__(self, fornecedor_nome,fornecedor_cnpj,fornecedor_cep,fornecedor_email,fornecedor_ddi,fornecedor_ddd,fornecedor_telefone,fornecedor_descricao):
        self.fornecedor_nome = fornecedor_nome
        self.fornecedor_cnpj = fornecedor_cnpj
        self.fornecedor_cep = fornecedor_cep
        self.fornecedor_email = fornecedor_email
        self.fornecedor_ddi = fornecedor_ddi
        self.fornecedor_ddd = fornecedor_ddd
        self.fornecedor_telefone = fornecedor_telefone
        self.fornecedor_descricao = fornecedor_descricao


    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            Validator.validar_nome(self.fornecedor_nome, "fornecedor_nome"),
            self.cnpj_existente(self.fornecedor_cnpj),
            Validator.validar_cpf_cnpj(self.fornecedor_cnpj, "fornecedor_cnpj"),
            Validator.validar_cep(self.fornecedor_cep, "fornecedor_cep"),
            self.email_existente(self.fornecedor_email),
            Validator.validar_email(self.fornecedor_email, "fornecedor_email"),
            Validator.validar_ddi_ddd(self.fornecedor_ddi, "fornecedor_ddi"),
            Validator.validar_ddi_ddd(self.fornecedor_ddd, "fornecedor_ddd"),
            Validator.validar_telefone(self.fornecedor_telefone, "fornecedor_telefone")
        ]
        
        for item in validacoes:
            if item is not None and not item['valida']:
                erros.append(item["mensagem"])

        return erros
    
    
    #Função para listar todos os fornecedores registrados
    @classmethod
    def listagem(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM fornecedor"
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
            raise ValueError("Fornecedor não encontrado.")
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o fornecedor porque ele está vinculado a outros serviços.")
        cls.delete(id)

    #Procura se o fornecedor em questão está relacionado com algum pedido de entrada
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM pedido_entrada WHERE fornecedor_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    
    #Procura no banco algum fornecedor com o mesmo CNPJ
    @classmethod
    def cnpj_existente(cls, cnpj):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True, buffered=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE fornecedor_cnpj = %s"
            cursor.execute(sql, (cnpj,))
            return cursor.fetchone() and {"valida":False, "mensagem":"CNPJ já existe no sistema"}
        finally:
            cursor.close()
            conexao.close()
    
    #Procura no banco algum fornecedor com o mesmo email
    @classmethod
    def email_existente(cls, email):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True, buffered=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE fornecedor_email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone() and {"valida":False, "mensagem":"Email já existe no sistema"}
        finally:
            cursor.close()
            conexao.close()