from models.funcionario import Funcionario
#importa a classe funcionario junto com as funções

dados = {
    "funcionario_nome": "Administrador",
    "funcionario_senha": "Admin123",
    "funcionario_cpf": "12345678900",
    "funcionario_cep": "13972398",
    "funcionario_email": "admin@sistema.com",
    "funcionario_ddi": "55",
    "funcionario_ddd": "19",
    "funcionario_telefone": "123456789",
    "funcionario_cargo": "Admin"
}
#dados de admin para iniciar o sistema

funcionario = Funcionario(**dados)
#juntando os dados dentro da classe funcionario pra inserir no banco
funcionario.inserir_funcionario()

print("Usuário administrador criado com sucesso.")