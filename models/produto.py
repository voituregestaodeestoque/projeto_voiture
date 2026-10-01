#faz todas as importações que iremos utilizar na classe Produto
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
import base64

class Produto(CrudBase):#cria a classe
    table = "produto"#nome da tabela
    fields = [
        'produto_nome',
        'produto_descricao', 
        'produto_categoria',
        'produto_quantidade_minima',
        'produto_preco_custo', 
        'produto_preco_venda',
        'produto_peso',
        'produto_localizacao',
        'imagem_nome',
        'imagem_tipo',
        'imagem_blob',
    ]#campos da tabela

    # metodo que cria um objeto 
    #o self passa os dados de cada campo
    def __init__(self, produto_nome, produto_descricao, produto_categoria, produto_quantidade_minima,
                 produto_preco_custo, produto_preco_venda, produto_peso, produto_localizacao,imagem_nome,imagem_tipo, imagem_blob):
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.produto_quantidade_minima = produto_quantidade_minima
        self.produto_preco_custo = produto_preco_custo
        self.produto_preco_venda = produto_preco_venda
        self.produto_peso = produto_peso
        self.produto_localizacao = produto_localizacao
        self.imagem_nome = imagem_nome
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob


    def validate(self): #validação
        erros = []

        validacoes = [
            Validator.required(self.produto_nome, "produto_nome"),
            Validator.validar_quantidade(self.produto_quantidade_minima, "produto_quantidade_minima"),
            Validator.validar_preco(self.produto_preco_custo, "produto_preco_custo"),
            Validator.validar_preco(self.produto_preco_venda, "produto_preco_venda"),
            Validator.validar_peso(self.produto_peso, "produto_peso"),
            Validator.validar_localizacao(self.produto_localizacao, "produto_localizacao")
        ]
        #Passa em cada item da lista com os retornos das validações
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"])

        return erros

    #função para listar os produtos registrados
    @classmethod
    def produto_listagem(cls):
        conexao = Database.connect() #conecta no banco
        cursor = conexao.cursor(dictionary=True)
        try:
            #Define o comando SQL que buscará todos os produtos
            sql = "SELECT * FROM produto"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close() #Desconecta do banco
            conexao.close()


    @classmethod
    #função que deleta oque não esta vinculado com outras tabelas
    def safe_delete(cls, id):
        produto = cls.find_by_id(id) #procura o id do produto
        if not produto: #não achou o produto
            raise ValueError("Produto não encontrado.")
        
        print(cls.has_related_records(id))
        if cls.has_related_records(id): #analisa se ta vinculado com outra tabela
            raise ValueError("Não é possível excluir o produto porque ele está vinculado a outros serviços.")
        cls.delete(id)

    #Define um método da classe
    @classmethod

    #define uma função
    def has_related_records(cls, id):

        #Conecta com o banco de dados
        conexao = Database.connect()

        #Ativa o cursor para selecionar linhas do banco de dados
        cursor = conexao.cursor()

        #Inicia uma tentativa
        try:
            #Monta uma lista que conta quantas vezes cliente aparece na tabela de pedido de entrada
            queries = [

                #Comando SQL para a contagem
                "SELECT COUNT(*) FROM detalhe_entrada WHERE produto_id = %s",
                "SELECT COUNT(*) FROM detalhe_saida WHERE produto_id = %s"
            ]
            #Define a quantidade inicial como zero
            total = 0

            #executará cada comando da lista de comandos
            for sql in queries:

                #executa o comando SQL
                cursor.execute(sql, (id,))

                #Soma a contagem do SQL à quantidade inicial
                total += cursor.fetchone()[0]

            #Retorna a soma maior que zero
            return total > 0
        
        #Enecerra a execução
        finally:

            #Fecha o cursor
            cursor.close()

            #Encerra a conexão
            conexao.close()
    

    @classmethod
    #função que conta
    def produto_total(cls):
        conexao = Database.connect()#conecta no banco
        cursor = conexao.cursor(dictionary=True)
        try:
            #conta quantos produtos tem no banco
            sql = "SELECT COUNT(produto_nome) as quantidade_produto FROM produto"
            cursor.execute(sql)
            return cursor.fetchone()
        finally:
            cursor.close()#fecha a conexão
            conexao.close()