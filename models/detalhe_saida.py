#importações que iremos utilizar na classe detalhe_saida
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_saida import Pedido_saida
from models.produto import Produto

#classe detalhe_saida
class Detalhe_saida(CrudBase):
    table = "detalhe_saida"
    fields = [
        'detalhe_saida_quantidade',
        'produto_id',
        'detalhe_saida_item',
        'pedido_saida_id'
    ]

    #define os valores para cada campo
    def __init__(self, detalhe_saida_quantidade, produto_id, detalhe_saida_item, pedido_saida_id):
        self.detalhe_saida_quantidade = detalhe_saida_quantidade
        self.produto_id = produto_id
        self.detalhe_saida_item = detalhe_saida_item
        self.pedido_saida_id = pedido_saida_id

    #função de validação
    def validate(self):
        erros = []
        #valida cada campo da tabela
        validacoes = [
            Validator.required(self.detalhe_saida_quantidade, "detalhe_saida_quantidade"),
            Validator.required(self.produto_id, "produto_id"),
            Validator.required(self.pedido_saida_id, "pedido_saida_id"),
        ]
        #verifica todos os itens validados
        for itens in validacoes:
            if not itens['valida']:
                erros.append(itens["mensagem"]) #adiciona em uma lista todas as mensagens de erro

        return erros

    #método para encontrar todas as informações de um pedido pelo id
    @classmethod
    def find_by_pedido(cls, pedido_saida_id):
        conexao = Database.connect() #conecta com o banco
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario

        #tenta encontrar todas as informações daquele pedido
        try:
            sql = """
            SELECT
            detalhe_saida.id,
            detalhe_saida.pedido_saida_id,
            detalhe_saida.produto_id,
            p.produto_nome AS produto,
            detalhe_saida.detalhe_saida_quantidade
            FROM detalhe_saida
            INNER JOIN produto p
            ON detalhe_saida.produto_id = p.id
            WHERE detalhe_saida.pedido_saida_id = %s
            ORDER BY detalhe_saida.id
            """
            cursor.execute(sql, (pedido_saida_id,)) #executa o comando sql
            return cursor.fetchall() #retorna todas as linhas após o comando sql
        finally:
            cursor.close()
            conexao.close()

    #método para adicionar item no pedido
    @classmethod

    #função que adiciona o item e requer quantidade, id do produto, item e id do pedido
    def adicionar_item(cls, detalhe_saida_quantidade, produto_id, detalhe_saida_item, pedido_saida_id):
        print("pedido", pedido_saida_id)
        pedido = Pedido_saida.find_by_id(pedido_saida_id)

        if not pedido: #se não encontrar o pedido
            return "Pedido não encontrado."

        if pedido["status_pedido_saida"] != "PENDENTE": #se o status for diferente de pendente
            return "Não é possível alterar um pedido finalizado."

        produto = Produto.find_by_id(produto_id) #encontra produto pelo id

        if not produto: #se não encontrar o produto
            return "Produto não encontrado."

        if detalhe_saida_quantidade <= 0: #se a quantidade de produto for menor ou igual a zero
            return "A quantidade deve ser maior que zero."

        #cria um objeto com os dados anteriores
        detalhe = cls(
            detalhe_saida_quantidade,
            produto_id,
            detalhe_saida_item,
            pedido_saida_id
        )
        print("detalhe", detalhe)
        erros = detalhe.validate() #valida os campos
        if erros: #se tiver erro
            return erros[0] #retorna o primeiro erro encontrado
        
        detalhe.insert() #insere as informações no detalhe_saida
        return "Item adicionado ao pedido."

    #método para remover um item do pedido
    @classmethod
    #função para remover o item de acordo com o id do detalhe saida
    def remover_item(cls, detalhe_saida_id):
        conexao = Database.connect() #conecta com o banco
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario

        try:
            #executa comando sql
            cursor.execute(
                "SELECT * FROM detalhe_saida WHERE id = %s",
                (detalhe_saida_id,) #verifica se tem alguma linha no detalhe saida
            )
            item = cursor.fetchone() #pega apenas uma linha

            if not item: #se não encontrar o item
                return "Item não encontrado."

            pedido_saida_id = item["pedido_saida_id"] #guarda o id do pedido

            cursor.execute(
                "DELETE FROM detalhe_saida WHERE id = %s",
                (detalhe_saida_id,) #deleta uma linha comparando o id
            )
            conexao.commit() #salva as informações

            return "Item removido com sucesso."

        except Exception: #se acontecer algum erro no try
            conexao.rollback() #desfaz qualquer rascunho que já tenha sido executado
            return "Erro ao remover item."
        finally: #encerra função
            cursor.close() #fecha o objeto cursor
            conexao.close() #encerra conexão

    