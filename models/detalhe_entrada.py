from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator
from models.pedido_entrada import Pedido_entrada
from models.produto import Produto


#CLASSE DETALHE_ENTRADA

class Detalhe_entrada(CrudBase): #cria a classe do detalhe entrada
    table = "detalhe_entrada" #nome da tabela
    fields = [
        'detalhe_entrada_quantidade',
        'produto_id',
        'detalhe_entrada_item',
        'pedido_entrada_id'
    ]




    #define os valores para cada campo
    def __init__(self, detalhe_entrada_quantidade, produto_id, detalhe_entrada_item, pedido_entrada_id ):
        self.detalhe_entrada_quantidade = detalhe_entrada_quantidade
        self.produto_id = produto_id
        self.detalhe_entrada_item = detalhe_entrada_item
        self.pedido_entrada_id = pedido_entrada_id
        
        
        

    #função de validação
    def validate(self):
        erros = []
        #valida cada campo da tabela
        validacoes = [
            Validator.required(self.detalhe_entrada_quantidade, "detalhe_entrada_quantidade"),
            Validator.required(self.produto_id, "produto_id"),
            Validator.required(self.pedido_entrada_id, "pedido_entrada_id"),
        ]
        #verifica todos os itens validados
        for itens in validacoes:
            if not itens['valida']: #verifica se o retorno é False
                erros.append(itens["mensagem"]) #adiciona em uma lista todas as mensagens de erro

        return erros




    #método para encontrar todas as informações de um pedido pelo id
    @classmethod
    def find_by_pedido(cls, pedido_entrada_id): #função para encontrar o pedido pelo id
        conexao = Database.connect() #conecta com o banco
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario

        try: #tenta encontrar todas as informações daquele pedido
            sql = """
            SELECT 
            detalhe_entrada.id,
            detalhe_entrada.pedido_entrada_id,
            detalhe_entrada.produto_id,
            p.produto_nome AS produto,
            detalhe_entrada.detalhe_entrada_quantidade
            FROM detalhe_entrada 
            INNER JOIN produto p
            ON detalhe_entrada.produto_id = p.id
            WHERE detalhe_entrada.pedido_entrada_id = %s
            ORDER BY detalhe_entrada.id
            """
            cursor.execute(sql, (pedido_entrada_id,)) #executa o comando sql
            return cursor.fetchall() #retorna todas as linhas após o comando sql
        
        finally: #encerra função
            cursor.close() #fecha o objeto cursor
            conexao.close() #encerra conexão





    #método para adicionar item no pedido
    @classmethod
    #função que adiciona o item e requer quantidade, id do produto, item e id do pedido
    def adicionar_item(cls, detalhe_entrada_quantidade, produto_id,  detalhe_entrada_item, pedido_entrada_id ):
        pedido = Pedido_entrada.find_by_id(pedido_entrada_id) #procura o pedido pelo id
        
        if not pedido: #se não encontrar o pedido
            return "Pedido não encontrado."

        if pedido["status_pedido_entrada"] != "PENDENTE": #se o status do pedido for diferente de PENDENDTE
            return "Não é possível alterar um pedido concluído ou cancelado."

        produto = Produto.find_by_id(produto_id) #procura o produto pelo id

        if not produto: #se não encontrar o produto
            return "Produto não encontrado."

        if detalhe_entrada_quantidade <= 0: #se a quantidade de produtos for menor ou igual a zero
            return "A quantidade deve ser maior que zero."

        detalhe = cls( #cria um objeto com os dados anteriores
        detalhe_entrada_quantidade,
        produto_id,
        detalhe_entrada_item,
        pedido_entrada_id
        )
        erros = detalhe.validate() #valida os campos
        if erros: #se tiver erro
            return erros[0] #retorna o primeiro erro encontrado
        
        detalhe.insert()  #insere as informações no detalhe_entrada
        return "Item adicionado ao pedido."





    #método para remover item do pedido
    @classmethod
    def remover_item(cls, detalhe_entrada_id): #função para remover o item de acordo com o id do detalhe entrada
        conexao = Database.connect() #conecta com o banco
        cursor = conexao.cursor(dictionary=True) #cursor executa comando SQL no banco e dictionary = True faz com que retorne em dicionario

        try:
            cursor.execute( #executa o comando sql
                "SELECT * FROM detalhe_entrada WHERE id = %s",
                (detalhe_entrada_id,) #verifica se tem alguma linha no detalhe entrada
            )
            item = cursor.fetchone() #pega apenas uma linha

            if not item: #se não encontrar
                return "Item não encontrado."

            pedido_entrada_id = item["pedido_entrada_id"] #guarda o id do pedido

            pedido = Pedido_entrada.find_by_id(pedido_entrada_id) #busca o pedido pelo id

            if pedido and pedido["status_pedido_entrada"] != "PENDENTE": #verifica se o status do pedido é diferente de pendente
                return "Não é possível remover itens de um pedido que não está pendente."

            cursor.execute( #executa o comando sql
                "DELETE FROM detalhe_entrada WHERE id = %s",
                (detalhe_entrada_id,) #deleta uma linha comparando o id
            )
            conexao.commit()#salva as informações

            return "Item removido com sucesso."

        except Exception: #se acontecer algum erro no try
            conexao.rollback() #desfaz qualquer rascunho que já tenha sido executado
            return "Erro ao remover item."
        finally: #encerra função
            cursor.close() #fecha o objeto cursor
            conexao.close() #encerra conexão
