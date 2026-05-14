
# Editado por Ryan em 12/05/2026 às 11:50

from flask import Flask, render_template, request, redirect, url_for, flash
from models.funcionario import Funcionario
from models.empilhadeira import Empilhadeira
from models.uso_empilhadeira import Uso_empilhadeira
from models.fornecedor import Fornecedor
from models.produto import Produto
from models.cliente import Cliente

app = Flask(__name__)
app.secret_key = "chave_secreta"

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

@app.route("/")
def inicio():
    return redirect(url_for("base"))

@app.route('/cadastroproduto')
def produtos():
    return render_template('cadastroproduto.html')


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

#Landing Page

@app.route('/landingpage')
def landingpage():
    return render_template('lp.html')

'''Empilhadeira Ryan Ribeiro'''

# cadastrodeempilhadeira

@app.route('/cadastroempilhadeira')
def cadastroempilhadeira():
    return render_template('cadastroempilhadeira.html')

def get_empilhadeira_form():
    return {
        "empilhadeira_chassi": request.form.get("empilhadeira_chassi", "").strip(),
        "empilhadeira_modelo": request.form.get("empilhadeira_modelo", "").strip(),
        "empilhadeira_marca": request.form.get("empilhadeira_marca", "").strip()
    }

# Registro do fornecedor no banco de dados
@app.route("/salvar_empilhadeira", methods=["POST"])
def salvar_empilhadeira():
    dados = get_empilhadeira_form()
    empilhadeira = Empilhadeira(**dados)

    #Validação
    erros = empilhadeira.validate()

    if erros :
        for erro in erros:
            flash(erro,"erro")
        return render_template("cadastroempilhadeira.html", empilhadeiras=dados)

    #Cadastro
    try:
        empilhadeira.insert()
        flash("Empilhadeira cadastrada com sucesso.", "sucesso")
        return redirect(url_for("tabelaempilhadeira"))
    except Exception as e:
        flash(f"Erro ao cadastrar empilhadeira: {e}", "erro")
        return render_template("tabelaempilhadeira.html", empilhadeiras=dados)

#Edição de um fornecedor já cadastrado
@app.route("/editar_empilhadeira/<int:id>")
def editar_empilhadeira(id):
    empilhadeira = Empilhadeira.find_by_id(id)
    if not empilhadeira:
        flash("Empilhadeira não encontrada.", "erro")
        return redirect(url_for("taeblaempilhadeira"))
    return render_template("cadastroempilhadeira.html", empilhadeira=empilhadeira)

#Atualização do cadastro de uma empilhadeira
@app.route("/atualizar_empilhadeira/<int:id>", methods=["POST"])
def atualizar_empilhadeira(id):
    dados = get_empilhadeira_form()
    empilhadeira = Empilhadeira(**dados)

    #Validação dos campos
    erros = empilhadeira.validate()

    #Tratativa de erro
    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastroempilhadeira.html", empilhadeira=dados)

    #Procura da empilhadeira por id
    try:
        #ID não encontrado
        if not Empilhadeira.find_by_id(id):
            flash("Empilhadeira não encontrada.", "erro")
            return redirect(url_for("tabelaempilhadeira"))

        #Id encontrado, atualização possível
        empilhadeira.update(id)
        flash("Empilhadeira atualizada com sucesso.", "sucesso")
        return redirect(url_for("tabelaempilhadeira"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar empilhadeira: {e}", "erro")
        return render_template("tabelaempilhadeira.html", empilhadeira=dados)

# Deleta uma empilhadeira
@app.route("/deletar_empilhadeira/<int:id>")
def deletar_empilhadeira(id):
    #Tenta deletar
    try:
        Empilhadeira.safe_delete(id)
        flash("Empilhadeira excluída com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir empilhadeira: {e}", "erro")
    return redirect(url_for("tabelaempilhadeira"))



@app.route('/tabelaempilhadeira')
def tabelaempilhadeira():
    uso = Empilhadeira.tabelatudojunto()
    empilhadeiras=Empilhadeira.empilhadeirasemuso()
    return render_template(
        'tabelaempilhadeira.html',
        uso=uso,
        empilhadeiras=empilhadeiras
    )








@app.route("/base")
def base():
    return render_template("dashboard.html")

# Uso de Empilhadeira
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

@app.route("/listagem_produto")
def listar_produto():
    produtos = Produto.produto_listagem()
    return render_template(
        'listagem_produto.html',
        produto=produtos)



@app.route("/cadastrar_produto", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)

    erros = produto.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", produto=dados)

    try:
        produto.insert()
        flash("Produto cadastrado com sucesso.", "sucesso")
        return redirect(url_for("base"))
    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "erro")
        return render_template("cadastroproduto.html", produto=dados)


@app.route("/produto/editar/<int:id>")
def editar_produto(id):
    produto = Produto.find_by_id(id)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("listar_produto"))
    return render_template("cadastroproduto.html", produto=produto)


@app.route("/produto/atualizar/<int:id>", methods=["POST"])
def atualizar_produto(id):
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastroproduto.html", produto=dados)

    try:
        if not Produto.find_by_id(id):
            flash("Produto não encontrado.", "erro")
            return redirect(url_for("listar_produto"))

        produto.update(id)
        flash("Produto atualizado com sucesso.", "sucesso")
        return redirect(url_for("listar_produto"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar produto: {e}", "erro")
        return render_template("cadastroproduto.html", produto=dados)

#===================================================================================

#Funcionário


@app.route('/cadastro_funcionario')
def cadastro_funcionario():
    return render_template('cadastrofuncionario.html')

@app.route("/listagem_funcionario")
def listagem_funcionario():
    funcionario = Funcionario.funcionario_listagem()
    return render_template(
        'listagem_funcionario.html',
        funcionarios=funcionario)

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
        flash("Funcionário cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listagem_funcionario"))
    except Exception as e:
        flash(f"Erro ao cadastrar funcionario: {e}", "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)

@app.route("/editar_funcionario/<int:id>")
def editar_funcionario(id):
    funcionario = Funcionario.find_by_id(id)
    if not funcionario:
        flash("Funcionário não encontrado.", "erro")
        return redirect(url_for("listagem_funcionario"))
    return render_template("cadastrofuncionario.html", funcionario=funcionario)


@app.route("/atualizar_funcionario/<int:id>", methods=["POST"])
def atualizar_funcionario(id):
    dados = get_funcionario_form()
    funcionario = Funcionario(**dados)
    erros = funcionario.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastrofuncionario.html", funcionario=dados)

    try:
        if not Funcionario.find_by_id(id):
            flash("Funcionario não encontrado.", "erro")
            return redirect(url_for("listagem_funcionario"))

        funcionario.update(id)
        flash("Funcionário atualizado com sucesso.", "sucesso")
        return redirect(url_for("listagem_funcionario"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar funcionário: {e}", "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)

# Deleta um funcionario
@app.route("/deletar_funcionario/<int:id>")
def deletar_funcionario(id):
    #Tenta deletar
    try:
        Funcionario.safe_delete(id)
        flash("Funcionário excluído com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir funcionário: {e}", "erro")
    return redirect(url_for("listagem_funcionario"))

#=====================================================================================#

# cliente atualizado por Ryan dia 12/05/26 às 9:00

def get_cliente_form():
        return {
        "cliente_nome": request.form.get("cliente_nome", "").strip(),
        "cliente_cnpj": request.form.get("cliente_cnpj", "").strip(),
        "cliente_cep": request.form.get("cliente_cep", "").strip(),
        "cliente_email": request.form.get("cliente_email", "").strip(),
        "cliente_ddi": request.form.get("cliente_ddi", "").strip(),
        "cliente_ddd": request.form.get("cliente_ddi", "").strip(),
        "cliente_telefone": request.form.get("cliente_telefone", "").strip(),
        "cliente_descricao": request.form.get("funcionario_descricao", "").strip(),
    }

@app.route("/listagem_cliente")
def listagem_cliente():
    clientes = Cliente.cliente_listagem()
    return render_template(
        'listagem_cliente.html',
        clientes=clientes)

@app.route('/cliente')
def cliente():
    return render_template('cadastrocliente.html')

@app.route("/salvar_cliente", methods=["POST"])
def salvar_cliente():
    dados = get_cliente_form()
    cliente = Cliente(**dados)

    erros = cliente.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastrocliente.html", cliente=dados)

    try:
        cliente.insert()
        flash("Cliente cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listagem_cliente"))
    except Exception as e:
        flash(f"Erro ao cadastrar cliente: {e}", "erro")
        return render_template("cadastrocliente.html", cliente=dados)

#Edição de um cliente já cadastrado
@app.route("/editar_cliente/<int:id>")
def editar_cliente(id):
    cliente = Cliente.find_by_id(id)
    if not cliente:
        flash("Cliente não encontrado.", "erro")
        return redirect(url_for("listagem_cliente"))
    return render_template("cadastrocliente.html", cliente=cliente)

#Atualização do cadastro de um cliente
@app.route("/atualizar_cliente/<int:id>", methods=["POST"])
def atualizar_cliente(id):
    dados = get_cliente_form()
    cliente = Cliente(**dados)

    #Validação dos campos
    erros = cliente.validate()

    #Tratativa de erro
    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastrocliente.html", cliente=dados)

    #Procura do cliente por id
    try:
        #ID não encontrado
        if not Cliente.find_by_id(id):
            flash("Cliente não encontrado.", "erro")
            return redirect(url_for("listagem_fornecedor"))

        #Id encontrado, atualização possível
        cliente.update(id)
        flash("Cliente atualizado com sucesso.", "sucesso")
        return redirect(url_for("listagem_cliente"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar cliente: {e}", "erro")
        return render_template("cadastrocliente.html", cliente=dados)


# Deleta um cliente
@app.route("/deletar_cliente/<int:id>")
def deletar_cliente(id):
    #Tenta deletar
    try:
        Cliente.safe_delete(id)
        flash("Cliente excluído com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir cliente: {e}", "erro")
    return redirect(url_for("listagem_cliente"))


# -----> Fim: Cliente



# -----> Início: Fornecedor

# Rota para a tela de cadastro de fornecedor
@app.route('/fornecedor')
def fornecedor():
    return render_template('cadastrofornecedor.html')


# Resgate das informações do formulário de cadastro de fornecedor
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

# Registro do fornecedor no banco de dados
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
        return redirect(url_for("listagem_fornecedor"))
    except Exception as e:
        flash(f"Erro ao cadastrar fornecedor: {e}", "erro")
        return render_template("cadastrofornecedor.html", fornecedor=dados)


# Listagem de fornecedores cadastrados
@app.route('/listagem_fornecedor')
def listagem_fornecedor():
    fornecedores = Fornecedor.listagem()
    return render_template(
        'listagem_fornecedor.html',
        fornecedores=fornecedores
    )


#Edição de um fornecedor já cadastrado
@app.route("/editar_fornecedor/<int:id>")
def editar_fornecedor(id):
    fornecedor = Fornecedor.find_by_id(id)
    if not fornecedor:
        flash("Fornecedor não encontrado.", "erro")
        return redirect(url_for("listagem_fornecedor"))
    return render_template("cadastrofornecedor.html", fornecedor=fornecedor)

#Atualização do cadastro de um fornecedor
@app.route("/atualizar_fornecedor/<int:id>", methods=["POST"])
def atualizar_fornecedor(id):
    dados = get_fornecedor_form()
    fornecedor = Fornecedor(**dados)

    #Validação dos campos
    erros = fornecedor.validate()

    #Tratativa de erro
    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastrofornecedor.html", fornecedor=dados)

    #Procura do fornecedor por id
    try:
        #ID não encontrado
        if not Fornecedor.find_by_id(id):
            flash("Fornecedor não encontrado.", "erro")
            return redirect(url_for("listagem_fornecedor"))

        #Id encontrado, atualização possível
        fornecedor.update(id)
        flash("Fornecedor atualizado com sucesso.", "sucesso")
        return redirect(url_for("listagem_fornecedor"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar fornecedor: {e}", "erro")
        return render_template("cadastrofornecedor.html", fornecedor=dados)


# Deleta um fornecedor
@app.route("/deletar_fornecedor/<int:id>")
def deletar_fornecedor(id):
    #Tenta deletar
    try:
        Fornecedor.safe_delete(id)
        flash("Fornecedor excluído com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir fornecedor: {e}", "erro")
    return redirect(url_for("listagem_fornecedor"))


# -----> Fim: Fornecedor




# pedido de entrada e saida
@app.route('/pedidoentrada')
def pedidoentrada():
    return render_template('pedidoentrada.html', pedido_entrada=None)

@app.route('/pedidosaida')
def pedidosaida():
    return render_template('pedidosaida.html', pedido_saida=None)

def get_pedidoentrada_form():
    return {
        "pedidoentrada_produto": request.form.get("pedidoentrada_produto", "").strip(),
        "pedidoentrada_quantidade": to_int(request.form.get("pedidoentrada_quantidade"))
    }

@app.route("/cadastrar_pedidoentrada")
def salvar_pedidoentrada():
    print("ola clara")
    
    dados = get_pedidoentrada_form()
    print(dados)

    return render_template("dashboard.html")
    #pedidoentrada = Pedido_entrada(**dados)
    
    '''erros = produto.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", produto=dados)'''
    '''
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
    }'''

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