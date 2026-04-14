from flask import Flask, render_template, request, redirect, url_for, flash
from models.funcionario import Funcionario

app = Flask(__name__)
app.secret_key = "chave_secreta"

@app.route('/cadastrofuncionario')
def cadastro_funcionario():
    return render_template('cadastrofuncionario.html')

@app.route('/loginfuncionario')
def login_funcionario():
    return render_template('loginfuncionario.html')

@app.route('/landingpage')
def landingpage():
    return render_template('lp.html')

@app.route('/loginfunciona')
def login():
    email = request.form.get("funcionario_email")
    senha = request.form.get("funcionario_senha")


    sql="Select * from funcionario where funcionario_email = %s and funcionario_senha = %s"

    return redirect(url_for("menu"))

@app.route('/')
def inicio():
    return render_template("menu.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")
                           
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
    
    '''erros = funcionario.validate()
    if erros :
        for erro in erros:
            flash(erro, "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)'''
    
    try:
        funcionario.insert()
        flash("Funcionario cadastrado com sucesso.", "sucesso")
        return redirect(url_for("menu"))
    except Exception as e:
        flash(f"Erro ao cadastrar funcionario: {e}", "erro")
        return render_template("cadastrofuncionario.html", funcionario=dados)


if __name__ == "__main__":
    app.run(debug=True)