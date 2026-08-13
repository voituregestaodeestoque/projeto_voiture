
# Editado por Ryan em 11/08/2026 às 10h12
from core.security import login_obrigatorio, admin_obrigatorio
from flask import Flask, render_template, request, redirect, url_for, flash, json, session
from models.funcionario import Funcionario
from models.empilhadeira import Empilhadeira
from models.uso_empilhadeira import Uso_empilhadeira
from models.fornecedor import Fornecedor
from models.produto import Produto
from models.cliente import Cliente
from models.pedido_entrada import Pedido_entrada
from models.detalhe_entrada import Detalhe_entrada
from models.detalhe_saida import Detalhe_saida
from models.pedido_saida import Pedido_saida
from models.estoque import Estoque
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_secreta"

EXTENSOES_PERMITIDAS = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


def imagem_permitida(tipo_arquivo):
    return tipo_arquivo in EXTENSOES_PERMITIDAS

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


############################################################################################################
# -----> Início: Landing Page

@app.route('/landingpage')
def landingpage():
    return render_template('landing_page.html')

# -----> Fim: Landing Page
############################################################################################################


############################################################################################################
# -----> Início: Login

#entra no sistema e já vai na primeira tela do sistema, LOGIN
@app.route("/")
def inicio():
    if "usuario_id" in session: #se já estiver logado, não precisa de login
        return redirect(url_for("base"))
    
    return redirect(url_for("loginfuncionario")) #direciona para o rota loginfuncionario


@app.route('/loginfuncionario')
def loginfuncionario():
    return render_template('loginfuncionario.html')


@app.route('/loginfunciona', methods=["POST"])
def login():
    #pega o email e senha do usuário para procurar no banco se já existe um funcionário com as informações
    email = request.form.get("funcionario_email")   
    senha = request.form.get("funcionario_senha")

    funcionario = Funcionario.autenticar(email,senha) #procura no banco um funcionário que bate com a senha e o email passado antes

    if funcionario: #se achar um funcionario, faz o login
        #cria uma sessão no sistema para poder usar o site
        session["usuario_id"] = funcionario["id"]
        session["funcionario_nome"] = funcionario["funcionario_nome"]
        session["funcionario_permissao"] = funcionario["funcionario_permissao"]
        return redirect(url_for("base"))#retorna para o site
    #se a senha ou email não bater
    flash("Login e/ou senha inválidos","erro")
    return render_template("loginfuncionario.html")

#desloga do sistema
@app.route("/logout")
def logout():
    session.clear() #apaga as informações de dentro do sessão
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("loginfuncionario"))

# -----> Fim: Login
############################################################################################################

#-----> Início: Perfil

@app.route('/perfil')
@login_obrigatorio
def perfil():

    funcionario = Funcionario.find_by_id(session["usuario_id"])

    return render_template(
        'perfil.html',
        funcionario=funcionario
    )

#Para atualizar o perfil 
@app.route("/atualizar_perfil", methods=["POST"])
@login_obrigatorio
def atualizar_perfil():

    id = session["usuario_id"]

    dados = get_funcionario_form()

    funcionario = Funcionario(**dados)

    erros = funcionario.validate()

    if erros:

        for erro in erros:
            flash(erro, "erro")

        funcionario.id = id

        return render_template(
            "perfil.html",
            funcionario=funcionario
        )

    funcionario.update(id)

    flash("Perfil atualizado com sucesso.", "sucesso")

    return redirect(url_for("perfil"))

# -----> Fim: Perfil
################################################################

############################################################################################################
# -----> Início: Base

@app.route("/base")
@login_obrigatorio
def base():
    return redirect(url_for("dashboard"))

# -----> Fim: Base
############################################################################################################


############################################################################################################
# -----> Início: Dashboard

#Rota para a tela de dashboard
@app.route("/dashboard")

# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio

#Função que define as funcionalidades do dashboard
def dashboard():

    entrada = Pedido_entrada.total_entradas()
    saida = Pedido_saida.total_saidas()

    #Recebe a soma de todas as quantidades contidas no estoque
    dic_total=Estoque.estoque_total()

    #Seleciona a chave do estoque total na tabela temporária de contagem
    total_estoque = dic_total['quantidade_total']

    #Recebe a soma de todos os tipos de produtos cadastrados no sistema
    pod_total=Produto.produto_total()

    #Seleciona a chave de quantidade de produto na tabela temporária de contagem
    total_produto = pod_total['quantidade_produto']


    entrada_total = Pedido_entrada.contar_pedidoentrada()

    total_entrada = entrada_total['pedido_entrada_total']


    saida_total = Pedido_saida.contar_pedidosaida()

    total_saida = saida_total['pedido_saida_total']


    #Recebe os produtos que estão com estoque baixo
    baixo_estoque = Estoque.estoque_baixo()


    pedido_entrada_pendente= Pedido_entrada.pedidoentrada_pendente()

    pedido_saida_pendente= Pedido_saida.pedidosaida_pendente()


    #Retorna a tela renderizada com todos os valores anteriores informados
    return render_template('dashboard.html', total_estoque=total_estoque,total_produto=total_produto, baixo_estoque=baixo_estoque, total_entrada=total_entrada, pedido_entrada_pendente=pedido_entrada_pendente, total_saida=total_saida, pedido_saida_pendente=pedido_saida_pendente,entrada=entrada,saida=saida)

# -----> Fim: Dashboard
############################################################################################################


############################################################################################################
# -----> Início: Estoque

#Rota para a tela de estoque
@app.route("/listagem_estoque")

# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio

#Função que define a listagem do estoque em cards
def listagem_estoque():

    #Recebe os dados da barra de pesquisa
    pesquisa = get_pesquisa_estoque_form()

    #Caso haja uma pesquisa
    if pesquisa:
        #Atualiza os cards na tela para os correspondentes à pesquisa
        estoque = Estoque.card_estoque_pesquisa(pesquisa)

    #Caso nada tenha sido pesquisado
    else:
        #Gera os cards de todos os produtos em estoque
        estoque = Estoque.card_estoque()

    #Recebe os argumentos para o filtro de ordenação
    filtro = request.args.get("filtro", "adc-recente")

    #Caso a opção alfabética seja selecionada
    if filtro == "nome":
        #Chama a função de ordenar por ordem alfabética de nome
        estoque = Estoque.card_estoque_nome()

    #Caso a opção quantidade maior em estoque seja selecionada
    elif filtro == "maior":
        #Chama a função de ordenar por quantidade maior em estoque
        estoque = Estoque.card_estoque_maior()

    #Caso a opção quantidade menor em estoque seja selecionada
    elif filtro == "menor":
        #Chama a função de ordenar por quantidade menor em estoque
        estoque = Estoque.card_estoque_menor()
    
    #Caso a opção preço maior seja selecionada
    elif filtro == "preco-maior":
        #Chama a função de ordenar por preço maior
        estoque = Estoque.card_estoque_preco_maior()

    #Caso a opção preço menor seja selecionada    
    elif filtro == "preco-menor":
        #Chama a função de ordenar por preço menor
        estoque = Estoque.card_estoque_preco_menor()        

    #Retorna a renderização da tela com a ordenação escolhida
    return render_template(
        "estoque.html",
        estoque=estoque,
        filtro=filtro
    )

#Recolhe os dados do formulário de pesquisa
def get_pesquisa_estoque_form():
    #Coleta a chave de pesquisa como um argumento
    chave = {"chave_pesquisa": request.args.get("chave_pesquisa", "").strip()}
    #Retorna o argumento
    return chave

# -----> Fim: Estoque
############################################################################################################

        
############################################################################################################        
# -----> Início: Produto

@app.route('/produtos')
@login_obrigatorio
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
@login_obrigatorio
def listagem_produto():

    produtos = Produto.produto_listagem()
    return render_template('listagem_produto.html',
        produto=produtos)



@app.route("/salvar_produto", methods=["POST"])
@login_obrigatorio
def salvar_produto():
    arquivo = request.files.get("imagem")

    imagem_nome = None
    imagem_tipo = None
    imagem_blob = None

    if arquivo and arquivo.filename != "":
        if not imagem_permitida(arquivo.content_type):
            flash("Formato de imagem inválido. Use PNG, JPG, JPEG ou WEBP.", "danger")
            return redirect(url_for("listagem_produto"))

        imagem_nome = arquivo.filename
        imagem_tipo = arquivo.content_type
        imagem_blob = arquivo.read()

    
    dados = get_produto_form()

    dados["imagem_nome"] = imagem_nome
    dados["imagem_tipo"] = imagem_tipo
    dados["imagem_blob"] = imagem_blob

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
@login_obrigatorio
def editar_produto(id):
    produto = Produto.find_by_id(id)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("listagem_produto"))
    return render_template("cadastroproduto.html", produto=produto)


@app.route("/atualizar_produto/<int:id>", methods=["POST"])
@login_obrigatorio
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
@login_obrigatorio
def deletar_produto(id):
    #Tenta deletar
    try:
        if Produto.has_related_records(id):
            flash(
                "Não é possível excluir o produto porque ele está vinculado a outros serviços.","erro"
            )
            return redirect(url_for("listagem_produto"))

        Estoque.delete_by_produto(id)
        Produto.safe_delete(id)
        flash("Produto excluído com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "erro")
    return redirect(url_for("listagem_produto"))

# -----> Fim: Produto
############################################################################################################
        

############################################################################################################
# -----> Início: Pedido de entrada

@app.route("/pedidoentrada")
@login_obrigatorio
def pedidoentrada():
    return render_template(
        "pedidoentrada.html",
        pedidos=Pedido_entrada.find_all_ordered()
    )

@app.route("/entrada/<int:pedido_entrada_id>")
@login_obrigatorio
def detalhes_entrada(pedido_entrada_id):
    pedido = Pedido_entrada.find_by_id(pedido_entrada_id)

    if not pedido:
        flash("Pedido de entrada não encontrado.")
        return redirect(url_for("pedidoentrada"))

    return render_template(
        "detalhes_entrada.html",
        pedido=pedido,
        itens=Detalhe_entrada.find_by_pedido(pedido_entrada_id),
        produto=Produto.find_all(order_by="produto_nome")
    )


@app.route("/entrada/<int:pedido_entrada_id>/adicionar", methods=["POST"])
@login_obrigatorio
def adicionar_item_entrada(pedido_entrada_id):
    produto_id = int(request.form.get("produto_id", 0))
    detalhe_entrada_quantidade = int(request.form.get("quantidade", 0) or 0)
    detalhe_entrada_item = request.form.get("detalhe_entrada_item", "")

    # Buscamos quantos itens esse pedido já tem salvos no banco
    itens_existentes = Detalhe_entrada.find_by_pedido(pedido_entrada_id)
    # Ex: se o pedido já tem 2 itens, o próximo será o 3 (2 + 1)
    proximo_item_numero = len(itens_existentes) + 1
    
    mensagem = Detalhe_entrada.adicionar_item(
        pedido_entrada_id = pedido_entrada_id,
        produto_id=produto_id,
        detalhe_entrada_quantidade=detalhe_entrada_quantidade,
        detalhe_entrada_item= proximo_item_numero
    )

    flash(mensagem)
    return redirect(url_for("detalhes_entrada", pedido_entrada_id=pedido_entrada_id))


@app.route("/entrada/item/remover/<int:detalhe_entrada_id>/<int:pedido_entrada_id>")
@login_obrigatorio
def remover_item_entrada(detalhe_entrada_id, pedido_entrada_id):
    mensagem = Detalhe_entrada.remover_item(detalhe_entrada_id)
    flash(mensagem)
    return redirect(url_for("detalhes_entrada", pedido_entrada_id=pedido_entrada_id))


@app.route("/entrada/finalizar/<int:pedido_entrada_id>")
@login_obrigatorio
def finalizar_entrada(pedido_entrada_id):
    try:
        mensagem = Pedido_entrada.finalizar(pedido_entrada_id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao atualizar pedido de entrada: {e}", "erro")
    return redirect(url_for("pedidoentrada"))


@app.route("/editar_pedido_entrada/<int:pedido_entrada_id>")
@login_obrigatorio
def editar_entrada(pedido_entrada_id):
    pedido = Pedido_entrada.find_by_id(pedido_entrada_id)
    if not pedido:
        flash("Pedido de entrada não encontrado.", "erro")
        return redirect(url_for("detalhes_entrada"))
    return render_template("detalhes_entrada.html", pedido=pedido, itens=Detalhe_entrada.find_by_pedido(pedido_entrada_id),
        produto=Estoque.card_estoque_nome())


@app.route("/entrada/nova", methods=["GET", "POST"])
@login_obrigatorio
def nova_entrada():
    if request.method == "POST":
        fornecedor_id = int(request.form.get("fornecedor_id", 0))
        itens_json = request.form.get("itens_json", "[]")


        try:
            itens = json.loads(itens_json)
        except Exception:
            itens = []

   
        pedido = Pedido_entrada(status_pedido_entrada="PENDENTE",fornecedor_id=fornecedor_id, data_pedido_entrada=datetime.now())
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
            cont = 0
            teste = []
            
            for item in itens:
                cont += 1
                Detalhe_entrada.adicionar_item(
                    pedido_entrada_id=pedido_entrada_id,
                    produto_id=int(item["produto_id"]),
                    detalhe_entrada_item = cont,
                    detalhe_entrada_quantidade=int(item["quantidade"])
                )
            
                print("check", teste)
            flash("Pedido de entrada criado com sucesso.","sucesso")
            return redirect(url_for("pedidoentrada", pedido_entrada_id=pedido_entrada_id))

        except Exception:
            flash("Erro ao criar pedido de entrada.")
            return render_template(
                "formulario_pedidoentrada.html",
                pedidos=Pedido_entrada.find_all_ordered(),
                produto=Produto.find_all(),
                fornecedores = Fornecedor.find_all()
            )

    return render_template(
        "formulario_pedidoentrada.html",
        pedido=None,
        produto=Produto.find_all(),
        fornecedores = Fornecedor.find_all()
    )
    
    
@app.route("/pedido/processar/<int:pedido_entrada_id>")
@login_obrigatorio
def processar_pedido_entrada(pedido_entrada_id):
    try:
        mensagem = Pedido_entrada.processar(pedido_entrada_id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao processar pedido: {e}", "erro")
    return redirect(url_for("pedidoentrada"))

@app.route("/pedido/cancelar/<int:pedido_entrada_id>")
@login_obrigatorio
def cancelar_pedido_entrada(pedido_entrada_id):
    try:
        mensagem = Pedido_entrada.cancelar(pedido_entrada_id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao cancelar pedido: {e}", "erro")
    return redirect(url_for("pedidoentrada"))

# -----> Fim: Pedido de entrada
############################################################################################################


############################################################################################################
# -----> Início: Pedido de saída

@app.route("/pedidosaida")
@login_obrigatorio
def pedidosaida():
    return render_template( 
        "pedidosaida.html",
        pedidos=Pedido_saida.find_all_ordered()
    )

@app.route("/saida/<int:pedido_saida_id>")
@login_obrigatorio
def detalhes_saida(pedido_saida_id):
    pedido = Pedido_saida.find_by_id(pedido_saida_id)

    if not pedido:
        flash("Pedido de saída não encontrado.")
        return redirect(url_for("pedidosaida"))

    return render_template(
        "detalhes_saida.html",
        pedido=pedido,
        itens=Detalhe_saida.find_by_pedido(pedido_saida_id),
        produto=Estoque.card_estoque_nome()
    )


@app.route("/saida/<int:pedido_saida_id>/adicionar", methods=["POST"])
@login_obrigatorio
def adicionar_item_saida(pedido_saida_id):
    produto_id = int(request.form.get("produto_id", 0))
    detalhe_saida_quantidade = int(request.form.get("quantidade", 0) or 0)
    detalhe_saida_item = request.form.get("detalhe_saida_item", "")

    # Buscamos quantos itens esse pedido já tem salvos no banco
    itens_existentes = Detalhe_saida.find_by_pedido(pedido_saida_id)
    # Ex: se o pedido já tem 2 itens, o próximo será o 3 (2 + 1)
    proximo_item_numero = len(itens_existentes) + 1

    

    mensagem = Detalhe_saida.adicionar_item(
        pedido_saida_id=pedido_saida_id,
        produto_id=produto_id,
        detalhe_saida_quantidade=detalhe_saida_quantidade,
        detalhe_saida_item= proximo_item_numero,
    )

    flash(mensagem)
    return redirect(url_for("detalhes_saida", pedido_saida_id=pedido_saida_id))


@app.route("/saida/item/remover/<int:detalhe_saida_id>/<int:pedido_saida_id>")
@login_obrigatorio
def remover_item_saida(detalhe_saida_id, pedido_saida_id):
    mensagem = Detalhe_saida.remover_item(detalhe_saida_id)
    flash(mensagem)
    return redirect(url_for("detalhes_saida", pedido_saida_id=pedido_saida_id))


@app.route("/saida/finalizar/<int:pedido_saida_id>")
@login_obrigatorio
def finalizar_saida(pedido_saida_id):
    try:
        mensagem = Pedido_saida.finalizar(pedido_saida_id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao atualizar pedido de saida: {e}", "erro")
    return redirect(url_for("pedidosaida"))


@app.route("/editar_pedido_saida/<int:pedido_saida_id>")
@login_obrigatorio
def editar_saida(pedido_saida_id):
    pedido = Pedido_saida.find_by_id(pedido_saida_id)
    if not pedido:
        flash("Pedido de saida não encontrado.", "erro")
        return redirect(url_for("detalhes_saida"))
    return render_template("detalhes_saida.html", pedido=pedido, itens=Detalhe_saida.find_by_pedido(pedido_saida_id),
        produto=Estoque.card_estoque_nome())
    

@app.route("/saida/nova", methods=["GET", "POST"])
@login_obrigatorio
def nova_saida():
    if request.method == "POST":
        cliente_id = int(request.form.get("cliente_id", 0))
        itens_json = request.form.get("itens_json", "[]")

        try:
            itens = json.loads(itens_json)
        except Exception:
            itens = []

        pedido = Pedido_saida(status_pedido_saida="PENDENTE", cliente_id=cliente_id, data_pedido_saida = datetime.now())
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
                "pedidosaida.html",
                pedido=pedido,
                produto=Estoque.card_estoque_nome(),
                clientes=Cliente.find_all()
            )
        
        try:
            pedido_saida_id = pedido.insert()
            cont = 0
            teste = []
            print("antes itens", pedido_saida_id)
            for item in itens:
                cont += 1
                Detalhe_saida.adicionar_item(
                    detalhe_saida_quantidade=int(item["quantidade"]),
                    produto_id=int(item["produto_id"]),
                    detalhe_saida_item=cont,
                    pedido_saida_id=pedido_saida_id
                    
                )
            
            print("check", teste)
            flash("Pedido de saída criado com sucesso.","sucesso")
            return redirect(url_for("pedidosaida", pedido_saida_id=pedido_saida_id))

        except Exception as e:
            print("erro", e)
            flash("Erro ao criar pedido de saída.")
            return render_template(
                "formulario_pedidosaida.html",
                pedidos=Pedido_saida.find_all_ordered(),
                produto=Estoque.card_estoque_nome(),
                clientes=Cliente.find_all()
            )

    return render_template(
        "formulario_pedidosaida.html",
        pedido=None,
        produto=Estoque.card_estoque_nome(),
        clientes=Cliente.find_all()
    )



@app.route("/pedido_saida/processar/<int:pedido_saida_id>")
@login_obrigatorio
def processar_pedido_saida(pedido_saida_id):
    try:
        mensagem = Pedido_saida.processar(pedido_saida_id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        print("VALUE ERROR:", e)
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao processar pedido: {e}", "erro")
    return redirect(url_for("pedidosaida"))


@app.route("/pedido_saida/cancelar/<int:pedido_saida_id>")
@login_obrigatorio
def cancelar_pedido_saida(pedido_saida_id):
    try:
        mensagem = Pedido_saida.cancelar(pedido_saida_id)
        flash(mensagem, "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao cancelar pedido: {e}", "erro")
    return redirect(url_for("pedidosaida"))
    
# -----> Fim: Pedido Saída
############################################################################################################


############################################################################################################
# -----> Início: Empilhadeira

# cadastrodeempilhadeira

#essa rota transfere o usuario pra tela de cadastro de empilhadeira
@app.route('/cadastroempilhadeira')
@login_obrigatorio
def cadastroempilhadeira():
    return render_template('cadastroempilhadeira.html')
    
#função que pega todos os dados do formulário da empilhadeira
def get_empilhadeira_form():
    return {
        "empilhadeira_chassi": request.form.get("empilhadeira_chassi", "").strip(),
        "empilhadeira_modelo": request.form.get("empilhadeira_modelo", "").strip(),
        "empilhadeira_marca": request.form.get("empilhadeira_marca", "").strip()
    }

# Registro de empilhadeira no banco de dados
@app.route("/salvar_empilhadeira", methods=["POST"])
@login_obrigatorio
def salvar_empilhadeira():
    dados = get_empilhadeira_form() #pega os dados do formulário de empilhadeira e coloca dentro da variavel dados
    empilhadeira = Empilhadeira(**dados) #junta os dados com a classe formando a variavel com tudo certo para outros procedimentos

    #Validação
    erros = empilhadeira.validate()

    if erros : #se tiver algum erro dentro do validate, ele cai nesse if
        for erro in erros: #mostra erro por erro
            flash(erro,"erro")
        return render_template("cadastroempilhadeira.html", empilhadeiras=dados) #volta os erros para a tela do formulario das empilhadeiras

    chassi = request.form.get("empilhadeira_chassi", "").strip() #pega só o chassi do formulario
    chassi_cadastrado = Empilhadeira.chassi_existente(chassi) #faz a função que verifica se já existe uma empilhadeira com aquele chassi
    if chassi_cadastrado: #se tiver alguma empilhadeira com aquele chassi, cai nesse if 
        flash("Chassi já existe no sistema! ","erro")
        return render_template("cadastroempilhadeira.html",empilhadeiras=dados) #mostra o erro na tela

    #Cadastro - depois que passou de todas as validações, insere no banco
    try:
        empilhadeira.insert() #insere as informações no banco
        flash("Empilhadeira cadastrada com sucesso.", "sucesso")
        return redirect(url_for("tabelaempilhadeira")) #volta para a tela onde mostra as empilhadeiras 
    except Exception as e: #se não conseguir inserir, é um erro diferente dos possiveis e cai aqui
        flash(f"Erro ao cadastrar empilhadeira: {e}", "erro") #mostra o erro
        return render_template("tabelaempilhadeira.html", empilhadeiras=dados)

@app.route("/alternar_status_empilhadeira/<int:id>")
@login_obrigatorio
def alternar_status_empilhadeira(id):

    try:
        novo_status = Empilhadeira.alternar_status(id)

        flash(
            f"Status da empilhadeira alterado para {novo_status}.",
            "sucesso"
        )

    except ValueError as e:
        flash(str(e), "erro")

    except Exception as e:
        flash(f"Erro ao alterar status da empilhadeira: {e}", "erro")

    return redirect(url_for("tabelaempilhadeira"))

#Edição de uma empilhadeira já cadastrada
@app.route("/editar_empilhadeira/<int:id>")
@login_obrigatorio
def editar_empilhadeira(id):
    empilhadeira = Empilhadeira.find_by_id(id) #procura o id da empilhadeira que você clicou 
    if not empilhadeira: #se der algum erro e não achar
        flash("Empilhadeira não encontrada.", "erro")
        return redirect(url_for("tabelaempilhadeira"))
    return render_template("cadastroempilhadeira.html", empilhadeira=empilhadeira) #mostra a tela de informações de uma empilhadeira já cadastrada

#Atualização do cadastro de uma empilhadeira
@app.route("/atualizar_empilhadeira/<int:id>", methods=["POST"])
@login_obrigatorio
def atualizar_empilhadeira(id):
    dados = get_empilhadeira_form() #pega os dados do formulário de empilhadeira e coloca dentro da variavel dados
    empilhadeira = Empilhadeira(**dados) #junta os dados com a classe formando a variavel com tudo certo para outros procedimentos

    #Validação dos campos
    erros = empilhadeira.validate()

    #Tratativa de erro
    if erros: #se tiver algum erro dentro do validate, ele cai nesse if
        for erro in erros: #mostra erro por erro
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastroempilhadeira.html", empilhadeira=dados)

    #Procura da empilhadeira por id
    try:
        #ID não encontrado
        if not Empilhadeira.find_by_id(id): #se não encontrar o id da empilhadeira
            flash("Empilhadeira não encontrada.", "erro")
            return redirect(url_for("tabelaempilhadeira"))

        #Id encontrado, atualização possível
        empilhadeira.update(id) #encontrou a empilhadeira e atualiza os dados
        flash("Empilhadeira atualizada com sucesso.", "sucesso")
        return redirect(url_for("tabelaempilhadeira"))
    except Exception as e: #se não conseguir inserir, é um erro diferente dos possiveis e cai aqui
        dados["id"] = id
        flash(f"Erro ao atualizar empilhadeira: {e}", "erro") #mostra o erro
        return render_template("tabelaempilhadeira.html", empilhadeira=dados)

# Deleta uma empilhadeira
@app.route("/deletar_empilhadeira/<int:id>")
@login_obrigatorio
def deletar_empilhadeira(id):
    #Tenta deletar
    try:
        Empilhadeira.delete(id) #deleta a empilhadeira com parametro do id
        flash("Empilhadeira excluída com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir empilhadeira: {e}", "erro")
    return redirect(url_for("tabelaempilhadeira"))

@app.route('/tabelaempilhadeira')
@login_obrigatorio
def tabelaempilhadeira():
    uso = Empilhadeira.tabelatudojunto() #função select pra mostrar as empilhadeira que estão sendo utilizadas
    empilhadeiras=Empilhadeira.empilhadeirasemuso() #função select pra mostrar as empilhadeira que não estão sendo utilizadas
    return render_template(
        'tabelaempilhadeira.html',
        uso=uso,
        empilhadeiras=empilhadeiras
    )

# -----> Fim: Empilhadeira
############################################################################################################


############################################################################################################
# -----> Início: Uso de Empilhadeira

@app.route("/desocupar_empilhadeira/<int:id>")
@login_obrigatorio
def desocupar_empilhadeira(id):

    try:
        Uso_empilhadeira.delete(id)
        flash("Empilhadeira desocupada com sucesso.", "sucesso")

    except Exception as e:
        flash(f"Erro ao desocupar empilhadeira: {e}", "erro")

    return redirect(url_for("tabelaempilhadeira"))


@app.route('/usoempilhadeira')
@login_obrigatorio
def usoempilhadeira():
    #empilhadeira = Empilhadeira()
    lista_empilhadeiras = empilhadeira.query.all()
    return render_template('usoempilhadeira.html' ,empilhadeiras=lista_empilhadeiras)


def get_uso_empilhadeira_form():
    return {
        "uso_empilhadeira_datahora": datetime.now(),
        "funcionario_id": to_int(request.form.get("funcionario_id")),
        "empilhadeira_id": request.form.get("empilhadeira_id"),
    }

@app.route("/salvar_uso_empilhadeira", methods=["POST"])
@login_obrigatorio
def salvar_uso_empilhadeira():

    dados = get_uso_empilhadeira_form()
    print("empilhadeira ",dados)

    if not dados["empilhadeira_id"]:
        flash("Selecione uma empilhadeira.", "erro")
        return redirect(url_for("usoempilhadeira"))

    if not dados["funcionario_id"]:
        flash("Selecione um funcionário.", "erro")
        return redirect(url_for("usoempilhadeira"))

    uso_empilhadeira = Uso_empilhadeira(**dados)

    try:
        uso_empilhadeira.insert()
        flash("Uso de empilhadeira cadastrado com sucesso.", "sucesso")
        return redirect(url_for("tabelaempilhadeira"))

    except Exception as e:
        flash(f"Erro ao cadastrar uso de empilhadeira: {e}", "erro")
        return redirect(url_for("usoempilhadeira"))
    
@app.route('/uso_empilhadeira_estrangeiro')
@login_obrigatorio
def uso_empilhadeira():

    funcionarios = Funcionario.funcionario_listagem()
    empilhadeiras = Empilhadeira.find_all()
    
    return render_template('usoempilhadeira.html',
     funcionarios=funcionarios,
     empilhadeiras=empilhadeiras
)


@app.route('/seu-formulario')
@login_obrigatorio
def exibir_formulario():
    lista_empilhadeiras = empilhadeira.query.all() 
    return render_template('usoempilhadeira.html', empilhadeiras=lista_empilhadeiras)

# -----> Fim: Uso de Empilhadeira
############################################################################################################


############################################################################################################
# -----> Início: Cliente

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
@login_obrigatorio
def listagem_cliente():
    clientes = Cliente.cliente_listagem()
    return render_template(
        'listagem_cliente.html',
        clientes=clientes)

@app.route('/cliente')
@login_obrigatorio
def cliente():
    return render_template('cadastrocliente.html')

@app.route("/salvar_cliente", methods=["POST"])
@login_obrigatorio
def salvar_cliente():
    dados = get_cliente_form()
    cliente = Cliente(**dados)

    numeros_cnpj = ""
    for caractere in cliente.cliente_cnpj:
        if caractere.isdigit():
            numeros_cnpj = numeros_cnpj + caractere
    cliente.cliente_cnpj = numeros_cnpj

    erros = cliente.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastrocliente.html", cliente=dados)

    cnpj = request.form.get("cliente_cnpj", "").strip()
    cnpj_cadastrado = Cliente.cnpj_existente(cnpj)
    if cnpj_cadastrado:
        flash("CNPJ já existe no sistema! ","erro")
        return render_template("cadastrocliente.html", cliente=dados)

    email = request.form.get("cliente_email", "").strip()
    email_cadastrado = Cliente.email_existente(email)
    if email_cadastrado:
        flash("Email já existe no sistema!","erro")
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
@login_obrigatorio
def editar_cliente(id):
    cliente = Cliente.find_by_id(id)
    if not cliente:
        flash("Cliente não encontrado.", "erro")
        return redirect(url_for("listagem_cliente"))
    return render_template("cadastrocliente.html", cliente=cliente)

#Atualização do cadastro de um cliente
@app.route("/atualizar_cliente/<int:id>", methods=["POST"])
@login_obrigatorio
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
@login_obrigatorio
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
############################################################################################################


############################################################################################################
# -----> Início: Fornecedor

# Rota para a tela de cadastro de fornecedor
@app.route('/fornecedor')
# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio

#função que renderiza o html da tela para cadastro
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
# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio

def salvar_fornecedor():
    #Recebe os dados resgatados do formulário
    dados = get_fornecedor_form()

    #Transforma as chaves em argumentos
    fornecedor = Fornecedor(**dados)

    numeros_cnpj = ""
    for caractere in fornecedor.fornecedor_cnpj:
        if caractere.isdigit():
            numeros_cnpj = numeros_cnpj + caractere
    fornecedor.fornecedor_cnpj = numeros_cnpj

    #Validação
    erros = fornecedor.validate()

    #Caso haja erros
    if erros :

        #Passa por todos as mensagens de erro da validação
        for erro in erros:
            #Apresenta a mensagem de erro
            flash(erro,"erro")

        #Retorna a tela renderizada com as mensagens
        return render_template("cadastrofornecedor.html", fornecedor=dados)

    #Coleta os dados de CNPJ do formulário
    cnpj = request.form.get("fornecedor_cnpj", "").strip()

    #Valida se o CNPJ já está cadastrado no sistema
    cnpj_cadastrado = Fornecedor.cnpj_existente(cnpj)

    #Caso já esteja cadastrado
    if cnpj_cadastrado:
        #Mensagem de erro
        flash("CNPJ já existe no sistema! ","erro")

        #Retorna a tela renderizada com as mensagens
        return render_template("cadastrofornecedor.html",fornecedor=dados)

    #Coleta os dados de email do formulário
    email = request.form.get("fornecedor_email", "").strip()

    #Valida se email já está cadastrado no sistema
    email_cadastrado = Fornecedor.email_existente(email)

    #Caso já esteja cadastrado
    if email_cadastrado:
        #Mensagem de erro
        flash("Email já existe no sistema!","erro")
        #Retorna a tela renderizada com as mensagens
        return render_template("cadastrofornecedor.html", fornecedor=dados)

    #Tentativa de cadastro
    try:
        #Executa a inserção
        fornecedor.insert()
        #Mensagem de sucesso
        flash("Fornecedor cadastrado com sucesso.", "sucesso")
        #Renderiza a tela de listagem com todos os fornecedores e a mensagem
        return redirect(url_for("listagem_fornecedor"))

    #Exceção: erros não tratado anteriormente
    except Exception as e:
        #Mensagem de erro
        flash(f"Erro ao cadastrar fornecedor: {e}", "erro")
        #Renderiza a tela com a mensagem de erro
        return render_template("cadastrofornecedor.html", fornecedor=dados)


# Listagem de fornecedores cadastrados
@app.route('/listagem_fornecedor')
# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio
def listagem_fornecedor():
    #Chama o método de listagem da classe Fornecedor
    fornecedores = Fornecedor.listagem()

    #Retorna a tela renderizadas com todos os fornecedores
    return render_template(
        'listagem_fornecedor.html',
        fornecedores=fornecedores
    )


#Edição de um fornecedor já cadastrado
@app.route("/editar_fornecedor/<int:id>")
# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio

def editar_fornecedor(id):
    #Seleciona um fornecedor pelo ID
    fornecedor = Fornecedor.find_by_id(id)

    #Caso não haja fornecedor com aquele ID
    if not fornecedor:
        #Mensagem de erro
        flash("Fornecedor não encontrado.", "erro")
        #Renderização da tela com o erro
        return redirect(url_for("listagem_fornecedor"))
    
    #Renderização da tela de edição
    return render_template("cadastrofornecedor.html", fornecedor=fornecedor)

#Atualização do cadastro de um fornecedor
@app.route("/atualizar_fornecedor/<int:id>", methods=["POST"])
# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio
def atualizar_fornecedor(id):

    #Recebe os dados resgatados do formulário
    dados = get_fornecedor_form()

    #Transforma as chaves em argumentos
    fornecedor = Fornecedor(**dados)

    #Validação dos campos
    erros = fornecedor.validate()

    #Tratativa de erro
    
    if erros:
        #Passa por todos as mensagens de erro da validação
        for erro in erros:
            #Apresenta a mensagem de erro
            flash(erro,"erro")

        #Coleta o parâmetro de ID    
        dados["id"] = id

        #Renderiza a tela com a mensagem 
        return render_template("cadastrofornecedor.html", fornecedor=dados)

    #Procura do fornecedor por id
    try:
        #ID não encontrado
        if not Fornecedor.find_by_id(id):
            #Mensagem de erro
            flash("Fornecedor não encontrado.", "erro")
            #Renderização da tela com a mensagem
            return redirect(url_for("listagem_fornecedor"))

        #Id encontrado, atualização possível
        fornecedor.update(id)
        #Mensagem de sucesso
        flash("Fornecedor atualizado com sucesso.", "sucesso")
        #Renderização da tela de listagem com todos os fornecedores e a mensagem
        return redirect(url_for("listagem_fornecedor"))

    #Exceção}: Erros não tratados anteriormente
    except Exception as e:
        dados["id"] = id
        #Mensagem de erro
        flash(f"Erro ao atualizar fornecedor: {e}", "erro")
        #Renderização da tela com a mensagem
        return render_template("cadastrofornecedor.html", fornecedor=dados)


# Deleta um fornecedor
@app.route("/deletar_fornecedor/<int:id>")
# Não é possível navegar por essa tela sem estar logado
@login_obrigatorio

def deletar_fornecedor(id):
    #Tenta deletar
    try:
        #Usa o método de deletar com segurança
        Fornecedor.safe_delete(id)
        #Mensagem de sucesso
        flash("Fornecedor excluído com sucesso.", "sucesso")

    #Tratativa de erros
    except ValueError as e:
        #Mensagem de erro
        flash(str(e), "erro")
    except Exception as e:
        #Mensagem de erro
        flash(f"Erro ao excluir fornecedor: {e}", "erro")
        
    #Renderização da tela de listagem com mensagem
    return redirect(url_for("listagem_fornecedor"))

# -----> Fim: Fornecedor
############################################################################################################


############################################################################################################
# -----> Início: Funcionário

# essa rota transfere o usuario pra tela de cadastro de funcionario
@app.route('/cadastro_funcionario')
@login_obrigatorio
def cadastro_funcionario():
    return render_template('cadastrofuncionario.html')

@app.route("/listagem_funcionario")
@login_obrigatorio
@admin_obrigatorio
def listagem_funcionario():
    funcionario = Funcionario.funcionario_listagem() #função select pra mostrar os funcionario cadastrados no sistema
    return render_template(
        'listagem_funcionario.html',
        funcionarios=funcionario)

#função que pega todos os dados do formulário do funcionário
def get_funcionario_form():
    return {
        "funcionario_nome": request.form.get("funcionario_nome", "").strip(),
        "funcionario_senha": request.form.get("funcionario_senha", "").strip(),
        "funcionario_cpf": request.form.get("funcionario_cpf", "").strip(),
        "funcionario_cep": request.form.get("funcionario_cep", "").strip(),
        "funcionario_email": request.form.get("funcionario_email", "").strip(),
        "funcionario_ddi": request.form.get("funcionario_ddi", "").strip(),
        "funcionario_ddd": request.form.get("funcionario_ddd", "").strip(),
        "funcionario_telefone": request.form.get("funcionario_telefone", "").strip(),
        "funcionario_cargo": request.form.get("funcionario_cargo", "").strip(),
        "funcionario_permissao": request.form.get("funcionario_permissao", "").strip(),
    }

# Registro de funcionário no banco de dados
@app.route("/salvar_funcionario", methods=["POST"])
@login_obrigatorio
def salvar_funcionario():
    print("FORM:", request.form)
    print("FILES:", request.files)
    print("CONTENT-TYPE:", request.content_type)
    arquivo = request.files.get("imagem")

    imagem_nome = None
    imagem_tipo = None
    imagem_blob = None

    if arquivo and arquivo.filename != "":
        if not imagem_permitida(arquivo.content_type):
            flash("Formato de imagem inválido. Use PNG, JPG, JPEG ou WEBP.", "danger")
            return redirect(url_for("listagem_produto"))

        imagem_nome = arquivo.filename
        imagem_tipo = arquivo.content_type
        imagem_blob = arquivo.read()
    dados = get_funcionario_form() #pega os dados do formulário do funcionário e coloca dentro da variavel dados

    dados["imagem_nome"] = imagem_nome
    dados["imagem_tipo"] = imagem_tipo
    dados["imagem_blob"] = imagem_blob
    funcionario = Funcionario(**dados)  #junta os dados com a classe formando a variavel com tudo certo para outros procedimentos
    numeros_cpf = ""
    for caractere in funcionario.funcionario_cpf:
        if caractere.isdigit():
            numeros_cpf = numeros_cpf + caractere
    funcionario.funcionario_cpf = numeros_cpf
    #Validação
    erros = funcionario.validate() 
    if erros: #se tiver algum erro dentro do validate, ele cai nesse if
        for erro in erros: #mostra erro por erro
            flash(erro, "erro")
        return render_template("cadastrofuncionario.html",funcionario=dados)

    cpf = request.form.get("funcionario_cpf","").strip() #pega só o cpf do formulario
    cpf_cadastrado = funcionario.cpf_existente(cpf) #faz a função que verifica se já existe um funcionario com aquele cpf
    if cpf_cadastrado: #se tiver algum funcionario com o cpf, cai nesse if 
        flash("CPF já cadastrado!", "erro")
        return render_template("cadastrofuncionario.html",funcionario=dados)

    email = request.form.get("funcionario_email","").strip() #pega só o email do formulario
    email_cadastrado = funcionario.email_existente(email) #faz a função que verifica se já existe um funcionario com aquele email
    if email_cadastrado: #se tiver algum funcionario com o email, cai nesse if 
        flash("Email já cadastrado!", "erro")
        return render_template("cadastrofuncionario.html",funcionario=dados)

    #Cadastro - depois que passou de todas as validações, insere no banco
    try:
        funcionario.inserir_funcionario() #insere as informações no banco com a senha criptografada
        flash("Funcionário cadastrado com sucesso.","sucesso")
        return redirect(url_for("listagem_funcionario"))

    except Exception as e: #se não conseguir inserir, é um erro diferente dos possiveis e cai aqui
        flash(f"Erro ao cadastrar funcionário: {e}","erro")
        return render_template("cadastrofuncionario.html",funcionario=dados)

#Edição de um funcionário já cadastrada
@app.route("/editar_funcionario/<int:id>")
@login_obrigatorio
def editar_funcionario(id):
    funcionario = Funcionario.find_by_id(id) #procura o id do funcionário que você clicou 
    if not funcionario: #se não achar o id do funcionario
        flash("Funcionário não encontrado.", "erro")
        return redirect(url_for("listagem_funcionario"))
    return render_template("cadastrofuncionario.html", funcionario=funcionario) #mostra a tela de informações de um funcionário já cadastrado


#Atualização do cadastro de um funcionário
@app.route("/atualizar_funcionario/<int:id>", methods=["POST"])
@login_obrigatorio
def atualizar_funcionario(id):
    dados = get_funcionario_form() #pega os dados do formulário do funcionário e coloca dentro da variavel dados
    funcionario = Funcionario(**dados) #junta os dados com a classe formando a variavel com tudo certo para outros procedimentos

    #Validação dos campos
    erros = funcionario.validate()

    #Tratativa de erro
    if erros: #se tiver algum erro dentro do validate, ele cai nesse if
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cadastrofuncionario.html", funcionario=dados)

    #Procura da empilhadeira por id
    try:
        #ID não encontrado
        if not Funcionario.find_by_id(id): #se não encontrar o id do funcionário
            flash("Funcionario não encontrado.", "erro")
            return redirect(url_for("listagem_funcionario"))

        #Id encontrado, atualização possível
        funcionario.update(id) #encontrou a empilhadeira e atualiza os dados
        flash("Funcionário atualizado com sucesso.", "sucesso")
        return redirect(url_for("listagem_funcionario"))
    except Exception as e: #se não conseguir inserir, é um erro diferente dos possiveis e cai aqui
        dados["id"] = id
        flash(f"Erro ao atualizar funcionário: {e}", "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)

# Deleta um funcionario
@app.route("/deletar_funcionario/<int:id>")
@login_obrigatorio
def deletar_funcionario(id):
    #Tenta deletar
    try:
        Funcionario.safe_delete(id) #deleta o funcionario com parametro do id
        flash("Funcionário excluído com sucesso.", "sucesso")
    #Tratativa de erro
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir funcionário: {e}", "erro")
    return redirect(url_for("listagem_funcionario"))

# -----> Fim: Funcionário
############################################################################################################


#Fim        

if __name__ == "__main__":
    app.run(debug=True)