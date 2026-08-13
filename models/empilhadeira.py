#faz todas as importações que iremos utilizar na classe empilhadeira
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Empilhadeira(CrudBase): #cria a classe empilhadeira
    table = "empilhadeira" #nome da tabela = empilhadeira
    fields = [
        "empilhadeira_chassi",
        "empilhadeira_status",
        "empilhadeira_modelo",
        "empilhadeira_marca"]
    
    #campos que existe na tabela
    
    #metodo pra criar um objeto e no self passando os dados de cada campo
    def __init__(self, empilhadeira_chassi, empilhadeira_status="INATIVA", empilhadeira_modelo="", empilhadeira_marca=""):
        self.empilhadeira_chassi = empilhadeira_chassi
        self.empilhadeira_status = empilhadeira_status
        self.empilhadeira_modelo = empilhadeira_modelo
        self.empilhadeira_marca = empilhadeira_marca

    #Função para validar os campos da tabela 
    def validate(self):
        erros = []

        #valida cada campo da tabela
        validacoes = [
            Validator.validar_chassi(self.empilhadeira_chassi, "empilhadeira_chassi"),
            Validator.validar_modelo(self.empilhadeira_modelo, "empilhadeira_modelo"),
            Validator.validar_marca(self.empilhadeira_marca, "empilhadeira_marca")
        ]
        #se der algum erro
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    #função que mostra as empilhadeiras que estão sendo utilizadas
    @classmethod
    def tabelatudojunto(cls):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True) #objeto
        try:
            #passa o select correto pra mostrar as empilhadeiras que estão sendo utilizadas
            sql = sql = """SELECT
    u.id AS uso_id,
    u.uso_empilhadeira_datahora,
    u.funcionario_id,
    u.empilhadeira_id,

    f.funcionario_nome,

    e.id AS empilhadeira_id_real,
    e.empilhadeira_chassi,
    e.empilhadeira_modelo,
    e.empilhadeira_marca,
    e.empilhadeira_status

FROM uso_empilhadeira u
INNER JOIN funcionario f
    ON u.funcionario_id = f.id
INNER JOIN empilhadeira e
    ON u.empilhadeira_id = e.id
WHERE u.funcionario_id IS NOT NULL
"""
            cursor.execute(sql) #executa o comando select
            return cursor.fetchall() #retorna as informações após o comando do sql
        finally: #fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    #função que mostra as empilhadeiras que não estão sendo utilizadas
    @classmethod
    def empilhadeirasemuso(cls):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True) #objeto
        try:
            #passa o select correto pra mostrar as empilhadeiras que não estão sendo utilizadas
            sql = """ SELECT e.* FROM empilhadeira e LEFT JOIN uso_empilhadeira u ON e.id = u.empilhadeira_id AND u.funcionario_id IS NOT NULL WHERE u.id IS NULL """
            cursor.execute(sql) #executa o comando sql do select
            return cursor.fetchall() #retorna os dados após o comando select
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    #Função para deletar com segurança
    @classmethod
    def safe_delete(cls, id):
        empilhadeira = cls.find_by_id(id) #procura o id da empilhadeira
        if not empilhadeira: #se não achar o id da empilhadeira
            raise ValueError("Empilhadeira não encontrada.")
        if cls.has_related_records(id): #verifica se essa empilhadeira está vinculada em mais de uma tabela
            raise ValueError("Não é possível excluir a empilhadeira porque ele está vinculado a outros serviços.")
        cls.delete(id) #deleta

    #função que verifica se a empilhadeira está em outra tabela
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor() 
        try:
            #conta quantas vezes existe o campo empilhadeira_id na tabela uso_emilhadeira
            queries = [
                "SELECT COUNT(*) FROM uso_empilhadeira WHERE empilhadeira_id = %s"
            ]
            total = 0
            for sql in queries: #percorre todos os comandos de dentro a tabela, porém nesse caso, só uma vez
                cursor.execute(sql, (id,)) #executa cada comando passando o id
                total += cursor.fetchone()[0] #pega a quantidade de vezes que encontrou do retorno e soma no total
            return total > 0 #se for maior que zero=True | se for menor que zero=False
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    #Procura no banco alguma empilhadeira com o mesmo chassi
    @classmethod
    def chassi_existente(cls, chassi):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True, buffered=True) #objeto
        try:
            #procura se existe uma empilhadeira com um chassi especifico
            sql = f"SELECT * FROM {cls.table} WHERE empilhadeira_chassi = %s"
            cursor.execute(sql, (chassi,)) #executa o query
            return cursor.fetchone() #retorna o resultado da query
        finally: # fecha o objeto e a conexão
            cursor.close()
            conexao.close()

    @classmethod
    #função para listar todas as empilhadeiras
    def empilhadeira_listagem(cls):
        return cls.find_all()

    @classmethod
    def alternar_status(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            # Busca o status atual
            sql = """
                SELECT empilhadeira_status
                FROM empilhadeira
                WHERE id = %s
            """

            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()

            if not resultado:
                raise ValueError("Empilhadeira não encontrada.")

            status_atual = resultado[0]

            # Alterna o status
            if status_atual == "ATIVA":
                novo_status = "INATIVA"
            else:
                novo_status = "ATIVA"

            # Atualiza o banco
            sql = """
                UPDATE empilhadeira
                SET empilhadeira_status = %s
                WHERE id = %s
            """

            cursor.execute(sql, (novo_status, id))
            conexao.commit()

            return novo_status

        finally:
            cursor.close()
            conexao.close()