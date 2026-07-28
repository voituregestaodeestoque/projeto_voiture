from models.funcionario import Funcionario
#importa a classe funcionario junto com as funções
from core.database import Database

def select_admin():
    conexao = Database.connect() #conecta no banco

    cursor = conexao.cursor(dictionary=True) #objeto

    try:
        #query select pra encontrar se existe algum funcionário com aquelas informações
        sql = f"""
            SELECT *
            FROM funcionario
            WHERE funcionario_nome = 'Administrador'
            """

        cursor.execute(sql) #executa o comando select
        funcionario = cursor.fetchall() #retorna as informações após o comando do sql
        if not funcionario: #se nao tiver nada em funcionario
            return None

        if funcionario:
            return funcionario

        return None

    finally: #fecha o objeto e a conexão
        cursor.close()
        conexao.close()

dados = {
    "funcionario_nome": "Administrador",
    "funcionario_senha": "Admin123",
    "funcionario_cpf": "12345678900",
    "funcionario_cep": "13972398",
    "funcionario_email": "admin@sistema.com",
    "funcionario_ddi": "55",
    "funcionario_ddd": "19",
    "funcionario_telefone": "123456789",
    "funcionario_cargo": "Admin",
    "funcionario_permissao": "administrador"
}

funcionario=select_admin()
if funcionario:
    print("Admin já cadastrado")
else:
    #dados de admin para iniciar o sistema
    funcionario = Funcionario(**dados)
    #juntando os dados dentro da classe funcionario pra inserir no banco
    funcionario.inserir_funcionario()
    print("Usuário administrador criado com sucesso.")