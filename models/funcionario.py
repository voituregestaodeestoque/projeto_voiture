from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from core.security import gerar_hash_senha, verificar_senha


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
    
    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        validacoes = [
            Validator.validar_nome(self.funcionario_nome, "funcionario_nome"),
            Validator.validar_senha(self.funcionario_senha, "funcionario_senha"),
            Validator.validar_cpf_cnpj(self.funcionario_cpf, "funcionario_cpf"),
            Validator.validar_cep(self.funcionario_cep, "funcionario_cep"),
            Validator.validar_email(self.funcionario_email, "funcionario_email"),
            Validator.validar_email(self.funcionario_email, "funcionario_email"),
            Validator.validar_ddi_ddd(self.funcionario_ddi, "funcionario_ddi"),
            Validator.validar_ddi_ddd(self.funcionario_ddd, "funcionario_ddd"),
            Validator.validar_telefone(self.funcionario_telefone, "funcionario_telefone"),
            Validator.validar_cargo(self.funcionario_cargo, "funcionario_cargo")
        ]
        
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    

    @classmethod
    def login(cls, email, senha):

        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM funcionario
                WHERE funcionario_email = %s
            """

            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario and verificar_senha(
                senha,
                usuario["funcionario_senha"]
            ):
                return usuario

            return None

        finally:
            cursor.close()
            conexao.close()

    #Função para listar todos os funcionarios registrados
    @classmethod
    def funcionario_listagem(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM funcionario"
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
            raise ValueError("Funcionario não encontrado.")
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o funcionario porque ele está vinculado a outros serviços.")
        cls.delete(id)

    #Procura se o funcionario em questão está relacionado com algum pedido de entrada
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM uso_empilhadeira WHERE funcionario_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    #Procura no banco algum funcionário com o mesmo CPF
    @classmethod
    def cpf_existente(cls, cpf):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True, buffered=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE funcionario_cpf = %s"
            cursor.execute(sql, (cpf,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()
    
    #Procura no banco algum funcionário com o mesmo email
    @classmethod
    def email_existente(cls, email):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True, buffered=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE funcionario_email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    
    def inserir_funcionario(self):

        self.funcionario_senha = gerar_hash_senha(
            self.funcionario_senha
        )

        return self.insert()

    def atualizar_funcionario(self, id_funcionario, dados):
        senha = dados.get("funcionario_senha")

        if senha:

            dados["funcionario_senha"] = gerar_hash_senha(
                senha
            )

        self.update(id_funcionario, dados)

    @classmethod
    def autenticar(cls, email, senha):
        """
        Verifica login do funcionário.
        """

        conexao = Database.connect()

        cursor = conexao.cursor(dictionary=True)

        try:

            sql = f"""
                SELECT *
                FROM {cls.table}
                WHERE funcionario_email = %s
            """

            cursor.execute(sql, (email,))
            funcionario = cursor.fetchone()


            if not funcionario:
                return None

            if verificar_senha(
                senha,
                funcionario["funcionario_senha"]
            ):
                return funcionario

            return None

        finally:

            cursor.close()
            conexao.close()