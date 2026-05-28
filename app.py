
# Editado por Júlia em 19/05/2026

from flask import Flask, render_template, request, redirect, url_for, flash
from models.funcionario import Funcionario
from models.empilhadeira import Empilhadeira
from models.uso_empilhadeira import Uso_empilhadeira
from models.fornecedor import Fornecedor
from models.produto import Produto
from models.cliente import Cliente
from models.pedido_entrada import Pedido_entrada
from models.detalhe_entrada import Detalhe_entrada
from models.estoque import Estoque

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

''' Dashboard '''


@app.route("/dashboard")
def dashboard():
    dic_total=Estoque.estoque_total()

    pod_total=Produto.produto_total()

    baixo_estoque = Estoque.estoque_baixo()

    total_produto = pod_total['quantidade_produto']
    total_estoque = dic_total['quantidade_total']
    return render_template('dashboard.html', total_estoque=total_estoque,total_produto=total_produto, baixo_estoque=baixo_estoque)


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

# Enderecamento
@app.route('/enderecamento')
def enderecamento():
    return render_template('enderecamento.html')

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
        
# -----> Início: Produto

@app.route('/produtos')
def produtos():
    return render_template('cadastroproduto.html')


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

def get_estoque_form():
    return{
        "estoque_quantidade":request.form.get("estoque_quantidade", "").strip()
    }

@app.route("/listagem_produto")
def listagem_produto():

    produtos = Produto.produto_listagem()
    return render_template('listagem_produto.html',
        produto=produtos)



@app.route("/salvar_produto", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)

    erros = produto.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", produto=dados)

    quantidade = get_estoque_form()
    estoque = Estoque(**quantidade)

    erros = estoque.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastroproduto.html", estoque = quantidade)

    try:
        prod_id = produto.insert()
        estoque.produto_id = prod_id
        if not prod_id == 0:
            estoque.insert()
        
        flash("Produto cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listagem_produto"))

    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "erro")
        return render_template("cadastroproduto.html", produto=dados)


@app.route("/editar_produto/<int:id>")
def editar_produto(id):
    produto = Produto.find_by_id(id)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("listagem_produto"))
    return render_template("cadastroproduto.html", produto=produto)


@app.route("/atualizar_produto/<int:id>", methods=["POST"])
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
            return redirect(url_for("listagem_produto"))

        produto.update(id)
        flash("Produto atualizado com sucesso.", "sucesso")
        return redirect(url_for("listagem_produto"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar produto: {e}", "erro")
        return render_template("cadastroproduto.html", produto=dados)


@app.route("/deletar_produto/<int:id>")
def deletar_produto(id):
    #Tenta deletar
    try:
        Produto.safe_delete(id)
        flash("Produto excluído com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "erro")
    return redirect(url_for("listagem_produto"))


# -----> Fim: Produto
#===================================================================================


# -----> Fim: Funcionário

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
    
    cpf=request.form.get("funcionario_cpf", "").strip()
    cpf1=funcionario.cpf_existente(cpf)
    if cpf1:
        flash("CPF já cadastrado!","erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)

    email=request.form.get("funcionario_email", "").strip()
    email1=funcionario.email_existente(email)
    if email1:
        flash("Email já cadastrado!","erro")
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

    cnpj = request.form.get("fornecedor_cnpj", "").strip()
    cnpj_cadastrado = fornecedor.cnpj_existente(cnpj)
    if cnpj_cadastrado:
        flash("CNPJ já existe no sistema! ","erro")
        return render_template("cadastrofornecedor.html",fornecedor=dados)

    email = request.form.get("fornecedor_email", "").strip()
    email_cadastrado = fornecedor.email_existente(email)

    if email_cadastrado:
        flash("Email já existe no sistema!","erro")
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




@app.route('/seu-formulario')
def exibir_formulario():
    lista_empilhadeiras = empilhadeira.query.all() 
    return render_template('usoempilhadeira.html', empilhadeiras=lista_empilhadeiras)
        

@app.route("/pedidoentrada")
def pedidoentrada():
    return render_template(
        "pedidoentrada.html",
        pedidos=Pedido_entrada.find_all_ordered()
    )



@app.route("/entrada/<int:pedido_entrada_id>")
def detalhes_entrada(pedido_entrada_id):
    pedido = Pedido_entrada.find_by_id(pedido_entrada_id)

    if not pedido:
        flash("Pedido de entrada não encontrado.")
        return redirect(url_for("pedidoentrada"))

    return render_template(
        "detalhes_entrada.html",
        pedido=pedido,
        itens=Detalhe_entrada.find_by_pedido(pedido_entrada_id),
        produto=Produto.find_all()
    )


@app.route("/entrada/<int:pedido_entrada_id>/adicionar", methods=["POST"])
def adicionar_item_entrada(pedido_entrada_id):
    produto_id = int(request.form.get("produto_id", 0))
    quantidade = int(request.form.get("quantidade", 0) or 0)

    mensagem = Detalhe_entrada.adicionar_item(
        pedido_id=pedido_entrada_id,
        produto_id=produto_id,
        quantidade=quantidade
    )

    flash(mensagem)
    return redirect(url_for("detalhes_entrada", pedido_entrada_id=pedido_entrada_id))


@app.route("/entrada/item/remover/<int:detalhe_entrada_id>/<int:pedido_entrada_id>")

def remover_item_entrada(detalhe_entrada_id, pedido_entrada_id):
    mensagem = Detalhe_entrada.remover_item(detalhe_entrada_id)
    flash(mensagem)
    return redirect(url_for("detalhes_entrada", pedido_entrada_id=pedido_entrada_id))


@app.route("/entrada/finalizar/<int:pedido_entrada_id>")
def finalizar_entrada(pedido_entrada_id):
    mensagem = Pedido_entrada.finalizar(pedido_entrada_id)
    flash(mensagem)
    return redirect(url_for("detalhes_entrada", pedido_entrada_id=pedido_entrada_id))


@app.route("/entrada/nova", methods=["GET", "POST"])
def nova_entrada():
    if request.method == "POST":
        fornecedor_id = int(request.form.get("fornecedor_id", 0))
        itens_json = request.form.get("itens_json", "[]")


        try:
            itens = json.loads(itens_json)
        except Exception:
            itens = []

        pedido = Pedido_entrada(status_pedido_entrada="PENDENTE",fornecedor_id=fornecedor_id)
        erros = pedido.validate()

        if not itens:
            erros.append("Adicione pelo menos um item ao pedido.")

        for item in itens:
            if int(item["quantidade"]) <= 0:
                erros.append("Todos os itens devem ter quantidade maior que zero.")

        if erros:
            for erro in erros:
                flash(erro)

            return render_template(
                "formulario_pedidoentrada.html",
                pedido=pedido,
                produto=Produto.find_all(),
                fornecedores=Fornecedor.find_all()
            )

        try:
            pedido_entrada_id = pedido.insert()

            for item in itens:
                Detalhe_entrada.adicionar_item(
                    pedido_entrada_id=pedido_entrada_id,
                    produto_id=int(item["produto_id"]),
                    quantidade=int(item["quantidade"])
                )


            flash("Pedido de entrada criado com sucesso.")
            return redirect(url_for("detalhes_entrada", pedido_entrada_id=pedido_entrada_id))

        except Exception:
            flash("Erro ao criar pedido de entrada.")
            return render_template(
                "pedidoentrada.html",
                pedidos=Pedido_entrada.find_all_ordered(),
                produto=Produto.find_all()

            )

    return render_template(
        "formulario_pedidoentrada.html",
        pedido=None,
        produto=Produto.find_all()
    )
'''Estoque'''

@app.route("/listagem_estoque")
def listagem_estoque():
    estoque=Estoque.card_estoque()
    return render_template('estoque.html', estoque=estoque)

@app.route('/uso_empilhadeira')
def uso_empilhadeira():
    # Buscamos a lista do banco usando a sua Classe (com E maiúsculo!)
    lista_de_maquinas = Empilhadeira.empilhadeirasemuso()
    
    # O nome que você coloca aqui antes do '=' é o que o HTML vai reconhecer
    return render_template('usoempilhadeira.html', empilhadeiras=lista_de_maquinas)
    
    try:
            uso_empilhadeira_id = uso_empilhadeira.insert()

            for item in itens:
                Itemuso_empilhadeira.adicionar_item(
                    uso_empilhadeira_id=uso_empilhadeira_id,
                    empilhadeira_id=int(item["empilhadeira_id"]),
                    empilhadeira_chassi=int(item["empilhadeira_chassi"]),
                    empilhadeira_modelo=item["empilhadeira_modelo"],
                    mpilhadeira_marca=item["empilhadeira_marca"]
                )

            uso_empilhadeira.atualizar_total(uso_empilhadeira_id)

    except Exception:
            flash("Erro ao criar uso_empilhadeira.")
            return render_template(
                "usoempilhadeira.html",
                uso_empilhadeira=uso_empilhadeira,
                empilhadeira=empilhadeira.find_all(order_by="nome")
            )

        

if __name__ == "__main__":
    app.run(debug=True)