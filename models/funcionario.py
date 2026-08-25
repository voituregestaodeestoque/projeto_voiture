#faz todas as importações que iremos utilizar na classe funcionario
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from core.security import gerar_hash_senha, verificar_senha
import base64


class Funcionario(CrudBase): #cria a classe empilhadeira
    table='funcionario' #nome da tabela
    fields=[
        'funcionario_nome',
        'funcionario_senha',
        'funcionario_cpf',
        'funcionario_cep',
        'funcionario_email',
        'funcionario_ddi',
        'funcionario_ddd',
        'funcionario_telefone',
        'funcionario_cargo',
        'funcionario_permissao',
        'funcionario_acesso',
        'imagem_nome',
        'imagem_tipo',
        'imagem_blob',
    ]
    #campos que existe na tabela

    #metodo pra criar um objeto e no self passando os dados de cada campo
    def __init__(self, funcionario_nome, funcionario_senha, funcionario_cpf, funcionario_cep, funcionario_email, funcionario_ddi, funcionario_ddd, funcionario_telefone, funcionario_cargo, funcionario_permissao,funcionario_acesso,imagem_nome=None,imagem_tipo=None, imagem_blob=None):
        self.funcionario_nome = funcionario_nome
        self.funcionario_senha = funcionario_senha
        self.funcionario_cpf = funcionario_cpf
        self.funcionario_cep = funcionario_cep
        self.funcionario_email = funcionario_email
        self.funcionario_ddi = funcionario_ddi
        self.funcionario_ddd = funcionario_ddd
        self.funcionario_telefone = funcionario_telefone
        self.funcionario_cargo = funcionario_cargo
        self.funcionario_permissao = funcionario_permissao
        self.funcionario_acesso = funcionario_acesso
        self.imagem_nome = imagem_nome
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob
    
    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        #valida cada campo da tabela
        validacoes = [
            Validator.validar_nome(self.funcionario_nome, "funcionario_nome"),
            Validator.validar_senha(self.funcionario_senha, "funcionario_senha"),
            Validator.validar_cpf(self.funcionario_cpf, "funcionario_cpf"),
            Validator.validar_cep(self.funcionario_cep, "funcionario_cep"),
            Validator.validar_email(self.funcionario_email, "funcionario_email"),
            Validator.validar_email(self.funcionario_email, "funcionario_email"),
            Validator.validar_ddi_ddd(self.funcionario_ddi, "funcionario_ddi"),
            Validator.validar_ddi_ddd(self.funcionario_ddd, "funcionario_ddd"),
            Validator.validar_telefone(self.funcionario_telefone, "funcionario_telefone"),
            Validator.validar_cargo(self.funcionario_cargo, "funcionario_cargo"),
            Validator.validar_permissao(self.funcionario_permissao, "funcionario_permissao"),
        ]
        #se der algum erro
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    @classmethod
    def preparar_imagens(cls, funcionarios):

        for funcionario in funcionarios:

            funcionario["imagem_base64"] = None

            if funcionario.get("imagem_blob"):
                funcionario["imagem_base64"] = base64.b64encode(
                    funcionario["imagem_blob"]
                ).decode("utf-8")

        return funcionarios

    @classmethod
    def preparar_imagem(cls, funcionario):

        #print("for ->", funcionario)
        funcionario["imagem_base64"] = None

        if funcionario.get("imagem_blob"):
            funcionario["imagem_base64"] = base64.b64encode(
                funcionario["imagem_blob"]
            ).decode("utf-8")

        return funcionario
    
    #função pra logar no sistema
    @classmethod
    def login(cls, email, senha):

        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True) #objeto

        try:
            #query select pra encontrar se existe algum funcionário com aquelas informações
            sql = """
                SELECT *
                FROM funcionario
                WHERE funcionario_email = %s
            """
            
            cursor.execute(sql, (email,)) #executa o comando select
            usuario = cursor.fetchone() #retorna as informações após o comando do sql

            #verifica se o usuario existe e se a senha está correta
            if usuario and verificar_senha( #aqui compara a senha digitada com a senha criptografada
                senha,
                usuario["funcionario_senha"]
            ):
                return usuario

            return None

        finally: #fecha o objeto e a conexão
            cursor.close() 
            conexao.close()

    #Função para listar todos os funcionarios registrados
    @classmethod
    def funcionario_listagem(cls ,):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True) #objeto
        try:
            #seleciona tudo de funcionario
            sql = "SELECT * FROM funcionario where id = %s"
            cursor.execute(sql) #executa o comando sql do select
            funcionarios = cursor.fetchall()
            return cls.preparar_imagens(funcionarios)  #retorna os dados após o comando select
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()
    
    @classmethod
    def funcionario_listagem_id(cls, id):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True) #objeto
        try:
            #seleciona tudo de funcionario pelo id
            sql = "SELECT * FROM funcionario where id = %s"
            cursor.execute(sql, (id,))
             #executa o comando sql do select
            funcionarios = cursor.fetchone()
            #print(funcionarios)
            return cls.preparar_imagem(funcionarios)  #retorna os dados após o comando select
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()


    #Função para deletar com segurança
    @classmethod
    def safe_delete(cls, id):
        funcionario = cls.find_by_id(id) #procura o id do funcionario
        if not funcionario: #se não achar o id do funcionario
            raise ValueError("Funcionario não encontrado.")
        if cls.has_related_records(id): #verifica se esse fucnionario está vinculado em alguma tabela
            raise ValueError("Não é possível excluir o funcionario porque ele está vinculado a outros serviços.")
        cls.delete(id)

    #Procura se o funcionario em questão está relacionado com algum uso de empilhadeira
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor()
        try:
            #conta quantas vezes existe o campo funcionario_id na tabela uso_empilhadeira
            queries = [
                "SELECT COUNT(*) FROM uso_empilhadeira WHERE funcionario_id = %s"
            ]
            total = 0
            for sql in queries: #percorre todos os comandos de dentro a tabela, porém nesse caso, só uma vez
                cursor.execute(sql, (id,)) #executa cada comando passando o id
                total += cursor.fetchone()[0] #pega a quantidade de vezes que encontrou do retorno e soma no total
            return total > 0 #se for maior que zero=True | se for menor que zero=False
        finally: #fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    #Procura no banco algum funcionário com o mesmo CPF
    @classmethod
    def cpf_existente(cls, cpf):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True, buffered=True) #objeto
        try:
            #procura se existe um funcionario com um cpf especifico
            sql = f"SELECT * FROM {cls.table} WHERE funcionario_cpf = %s"
            cursor.execute(sql, (cpf,)) #executa o query
            return cursor.fetchone() #retorna o resultado da query
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()
    
    #Procura no banco algum funcionário com o mesmo email
    @classmethod
    def email_existente(cls, email):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True, buffered=True) #objeto
        try:
            #procura se existe um funcionario com um email especifico
            sql = f"SELECT * FROM {cls.table} WHERE funcionario_email = %s"
            cursor.execute(sql, (email,)) #executa o query
            return cursor.fetchone() #retorna o resultado da query
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    
    def inserir_funcionario(self):

        self.funcionario_senha = gerar_hash_senha( #pega a senha digitada e criptografa ela
            self.funcionario_senha
        )
        #insere no banco a senha já criptografada
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

        conexao = Database.connect() #conecta no banco

        cursor = conexao.cursor(dictionary=True) #objeto

        try:
            #query select pra encontrar se existe algum funcionário com aquelas informações
            sql = f"""
                SELECT *
                FROM {cls.table}
                WHERE funcionario_email = %s
            """

            cursor.execute(sql, (email,)) #executa o comando select
            funcionario = cursor.fetchone() #retorna as informações após o comando do sql


            if not funcionario: #se nao tiver nada em funcionario
                return None

            if verificar_senha( #se a senha digitada bater com a criptografada
                senha,
                funcionario["funcionario_senha"]
            ):
                return funcionario

            return None

        finally: #fecha o objeto e a conexão

            cursor.close()
            conexao.close()

    #Procura no banco algum funcionário com o mesmo email
    @classmethod
    def email_existente(cls, email):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True, buffered=True) #objeto
        try:
            #procura se existe um funcionario com um email especifico
            sql = f"SELECT * FROM {cls.table} WHERE funcionario_email = %s"
            cursor.execute(sql, (email,)) #executa o query
            return cursor.fetchone() #retorna o resultado da query
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    #bloqueia o acesso do funcionario no login
    @classmethod
    def bloquear_acesso(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE funcionario
                SET funcionario_acesso = FALSE
                WHERE id = %s
            """

            cursor.execute(sql, (id,))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def desbloquear_acesso(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE funcionario
                SET funcionario_acesso = TRUE
                WHERE id = %s
            """

            cursor.execute(sql, (id,))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()