
#Editado por Júlia em 05/05/2026 às 13h55

from flask import Flask, render_template, request, redirect, url_for, flash
from models.funcionario import Funcionario
from models.empilhadeira import Empilhadeira
from models.uso_empilhadeira import Uso_empilhadeira
from models.fornecedor import Fornecedor

app = Flask(__name__)
app.secret_key = "chave_secreta"

@app.route('/cadastroproduto')
def produtos():
    return render_template('cadastroproduto.html')

@app.route('/cadastrofuncionario')
def cadastro_funcionario():
    return render_template('cadastrofuncionario.html')

'''Login funcionário - Ryan Ribeiro'''
@app.route('/loginfuncionario')
def loginfuncionario():
    return render_template('loginfuncionario.html')

@app.route('/loginfunciona')
def login():
    email = request.form.get("funcionario_email")
    senha = request.form.get("funcionario_senha")


    sql="Select * from funcionario where funcionario_email = %s and funcionario_senha = %s"

    return redirect(url_for("base"))

@app.route('/landingpage')
def landingpage():
    return render_template('lp.html')

@app.route('/tabelaempilhadeira')
def tabelaempilhadeira():
    uso = Empilhadeira.tabelatudojunto()
    empilhadeiras=Empilhadeira.empilhadeirasemuso()
    return render_template(
        'tabelaempilhadeira.html',
        uso=uso,
        empilhadeiras=empilhadeiras
    )



@app.route("/")
def inicio():
    return redirect(url_for("base"))

@app.route("/base")
def base():
    return render_template("dashboard.html")

#Uso de Empilhadeira
@app.route('/usoempilhadeira')
def usoempilhadeira():
    return render_template('usoempilhadeira.html')


def get_uso_empilhadeira_form():
    return {
        "funcionario_id": request.form.get("funcionario_id", "").strip(),
        "empilhadeira_id": request.form.get("empilhadeira_id", "").strip(),
    }

@app.route("/salvar_uso_empilhadeira", methods=["POST"])
def salvar_uso_empilhadeira():
    dados = get_uso_empilhadeira_form()
    uso_empilhadeira = Uso_empilhadeira(**dados)

    try:
        uso_empilhadeira.insert()
        flash("Uso  de Empilhadeira cadastrado com sucesso.", "sucesso")
        return redirect(url_for("base"))
    except Exception as e:
        flash(f"Erro ao cadastrar uso de empilhadeira{e}", "erro")
        return render_template("cadastro_uso_empilhadeira.html", fornecedor=dados)

#cadastrodeempilhadeira

def get_cadastroempilhaderia_form():
        return {
        "cadastroempilhadeira_numero_chassi": request.form.get("cadastroempilhadeira_numero_chassi", "").strip(),
        "cadastroempilhadeira_marca": request.form.get("cadastroempilhadeira_marca", "").strip(),
        "cadastroempilhadeira_modelo": request.form.get("cadastroempilhadeira_modelo", "").strip(),
    }

@app.route('/cadastroempilhadeira')
def cadastroempilhadeira():
    return render_template('cadastroempilhadeira.html')

@app.route("/salvar_cadastroempilhadeira", methods=["POST"])
def salvar_cadastroempilhadeira():
    dados = get_cadastroempilhadeira_form()
    cadastroempilhadeira = cadastroempilhadeira(**dados)
    
    '''erros = cadastroempilhadeira.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroempilhadeira.html", cadastroempilhadeira=dados)'''
    
    try:
        cadastroempilhadeira.insert()
        flash("cadastro de empilhadeira cadastrado com sucesso.", "sucesso")
        return redirect(url_for("menu"))
    except Exception as e:
        flash(f"Erro ao cadastrar empilhadeira: {e}", "erro")
        return render_template("cadastroempilhadeira.html", cadastroempilhadeira=dados)

def get_produto_form():
    return {
        "produto_nome": request.form.get("produto_nome", "").strip(),
        "produto_categoria": request.form.get("produto_categoria", "").strip(),
        "produto_localizacao": request.form.get("produto_localizacao", "").strip(),
        "produto_quantidade_minima": request.form.get("produto_quantidade_minima", "").strip(),
        "produto_peso": request.form.get("produto_peso", "").strip(),
        "produto_preco_custo": request.form.get("produto_preco_custo", "").strip(),
        "produto_preco_venda": request.form.get("produto_preco_venda", "").strip(),
        "produto_descricao": request.form.get("produto_descricao", "").strip(),
    }

@app.route("/cadastrar_produto", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)
    
    '''erros = produto.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", produto=dados)'''
    
    try:
        produto.insert()
        flash("Produto cadastrado com sucesso.", "sucesso")
        return redirect(url_for("menu"))
    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "erro")
        return render_template("cadastroproduto.html", produto=dados)

def get_funcionario_form():
    return {
        "funcionario_nome": request.form.get("funcionario_nome", "").strip(),
        "funcionario_senha": request.form.get("funcionario_senha", "").strip(),
        "funcionario_cpf": request.form.get("funcionario_cpf", "").strip(),
        "funcionario_cep": request.form.get("funcionario_cep", "").strip(),
        "funcionario_email": request.form.get("funcionario_email", "").strip(),
        "funcionario_ddi": request.form.get("funcionario_ddi", "").strip(),
        "funcionario_ddd": request.form.get("funcionario_ddi", "").strip(),
        "funcionario_telefone": request.form.get("funcionario_telefone", "").strip(),
        "funcionario_cargo": request.form.get("funcionario_cargo", "").strip(),
    }

@app.route("/salvar_funcionario", methods=["POST"])
def salvar_funcionario():
    dados = get_funcionario_form()
    funcionario = Funcionario(**dados)
    
    erros = funcionario.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)
    
    try:
        funcionario.insert()
        flash("Funcionario cadastrado com sucesso.", "sucesso")
        return redirect(url_for("base"))
    except Exception as e:
        flash(f"Erro ao cadastrar funcionario: {e}", "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)

#cliente

def get_cliente_form():
        return {
        "cliente_nome": request.form.get("cliente_nome", "").strip(),
        "cliente_senha": request.form.get("cliente_senha", "").strip(),
        "cliente_cnpj": request.form.get("cliente_cnpj", "").strip(),
        "cliente_cep": request.form.get("cliente_cep", "").strip(),
        "cliente_ddi": request.form.get("cliente_ddi", "").strip(),
        "cliente_ddd": request.form.get("cliente_ddi", "").strip(),
        "cliente_telefone": request.form.get("cliente_telefone", "").strip(),
        "cliente_descricao": request.form.get("funcionario_descricao", "").strip(),
    }

@app.route('/cliente')
def cliente():
    return render_template('cadastrocliente.html')

@app.route("/salvar_cliente", methods=["POST"])
def salvar_cliente():
    dados = get_cliente_form()
    cliente = cliente(**dados)
    
    '''erros = cliente.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cliente.html", cliente=dados)'''
    
    try:
        cliente.insert()
        flash("cliente cadastrado com sucesso.", "sucesso")
        return redirect(url_for("menu"))
    except Exception as e:
        flash(f"Erro ao cadastrar cliente: {e}", "erro")
        return render_template("cliente.html", cliente=dados)



#-----> Início: Fornecedor

#Rota para a tela de cadastro de fornecedor
@app.route('/fornecedor')
def fornecedor():
    return render_template('cadastrofornecedor.html')


#Resgate das informações do formulário de cadastro de fornecedor
def get_fornecedor_form():
    return {
        "fornecedor_nome": request.form.get("fornecedor_nome", "").strip(),
        "fornecedor_cnpj": request.form.get("fornecedor_cnpj", "").strip(),
        "fornecedor_cep": request.form.get("fornecedor_cep", "").strip(),
        "fornecedor_email": request.form.get("fornecedor_email", "").strip(),
        "fornecedor_ddi": request.form.get("fornecedor_ddi", "").strip(),
        "fornecedor_ddd": request.form.get("fornecedor_ddd", "").strip(),
        "fornecedor_telefone": request.form.get("fornecedor_telefone", "").strip(),
        "fornecedor_descricao": request.form.get("fornecedor_descricao", "").strip(),
    }

#Registro do fornecedor no banco de dados
@app.route("/salvar_fornecedor", methods=["POST"])
def salvar_fornecedor():
    dados = get_fornecedor_form()
    fornecedor = Fornecedor(**dados)

    #Validação
    erros = fornecedor.validate()
    
    if erros :
        for erro in erros:
            flash(erro,"erro")
        return render_template("cadastrofornecedor.html", fornecedor=dados)
    
    #Cadastro
    try:
        fornecedor.insert()
        flash("Fornecedor cadastrado com sucesso.", "sucesso")
        return redirect(url_for("base"))
    except Exception as e:
        flash(f"Erro ao cadastrar fornecedor: {e}", "erro")
        return render_template("cadastrofornecedor.html", fornecedor=dados)
    

#Listagem de fornecedores cadastrados
@app.route('/listagem_fornecedor')
def listagem_fornecedor():
    fornecedores = Fornecedor.listagem()
    return render_template(
        'listagem_fornecedor.html',
        fornecedores=fornecedores
    )

#-----> Fim: Fornecedor




#pedido de entrada e saida
@app.route('/pedidoentrada')
def pedidoentrada():
    return render_template('pedidoentrada.html', pedido_entrada=None)

@app.route('/pedidosaida')
def pedidosaida():
    return render_template('pedidosaida.html', pedido_saida=None)

def get_pedidoentrada_form():
    return {
        "pedidoentrada_produto": request.form.get("pedidoentrada_produto", "").strip(),
        "pedidoentrada_quantidade": request.form.get("pedidoentrada_quantidade", "").strip(),
        "pedidoentrada_fornecedor": request.form.get("pedidoentrada_fornecedor", "").strip()
    }

@app.route("/cadastrar_pedidoentrada", methods=["POST"])
def salvar_pedidoentrada():
    dados = get_pedidoentrada_form()
    pedidoentrada = Pedido_entrada(**dados)
    
    '''erros = produto.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", produto=dados)'''
    
    try:
        pedidoentrada.insert()
        flash("Pedido cadastrado com sucesso.", "sucesso")
        return redirect(url_for("menu"))
    except Exception as e:
        flash(f"Erro ao cadastrar pedido: {e}", "erro")
        return render_template("pedidoentrada.html", pedido_entrada=dados)

def get_pedidosaida_form():
    return {
        "pedidosaida_produto": request.form.get("pedidosaida_produto", "").strip(),
        "pedidosaida_quantidade": request.form.get("pedidosaida_quantidade", "").strip(),
        "pedidosaida_cliente": request.form.get("pedidosaida_cliente", "").strip()
    }

@app.route("/cadastrar_pedidosaida", methods=["POST"])
def salvar_pedidosaida():
    dados = get_pedidosaida_form()
    pedidosaida = Pedido_saida(**dados)
    
    '''erros = produto.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", produto=dados)'''
    
    try:
        pedidosaida.insert()
        flash("Pedido cadastrado com sucesso.", "sucesso")
        return redirect(url_for("menu"))
    except Exception as e:
        flash(f"Erro ao cadastrar pedido: {e}", "erro")
        return render_template("pedidosaida.html", pedido_saida=dados)

if __name__ == "__main__":
    app.run(debug=True)



@app.route("/cadastrar_pedidoentrada_lote", methods=["POST"])
def cadastrar_pedidoentrada_lote():
    data = request.get_json()

    fornecedor = data.get("fornecedor")
    itens = data.get("itens", [])

    try:
        for item in itens:
            pedido = Pedido_entrada(
                pedidoentrada_produto=item["produto"],
                pedidoentrada_quantidade=item["quantidade"],
                pedidoentrada_fornecedor=fornecedor
            )
            pedido.insert()

        return jsonify({"mensagem": "Pedido cadastrado com sucesso!"})

    except Exception as e:
        return jsonify({"mensagem": f"Erro: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)