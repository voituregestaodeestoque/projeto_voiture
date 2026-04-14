#imports
import requests
import urllib.parse

'''============> validarÇÕES BASE EXTERNAS <============'''

#função:validação externa de CEP
def validar_cep(cep):
    for caractere in cep["cep"]:
        if not(caractere.isdigit()):
            return False
    if  not len(cep["cep"]) == 8:
        return False
    base_url = "https://api.invertexto.com/v1/cep"
    cep_encoded = urllib.parse.quote(cep["cep"])
    url = f"{base_url}/{cep_encoded}"
    params = {"token":"22590|VRlqZZZ2IlPzK682Q8mjVW6n8SAwLWFO"}
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        retorno_cep = response.json()
        if retorno_cep:
            return True
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:",errt)
    except requests.exceptions.RequestException as err:
        print("Erro:", err)
    return False


#função:validação externa de email
def validar_email(email):
    base_url = "https://api.invertexto.com/v1/email-validator"
    email_encoded = urllib.parse.quote(email["email"])
    url = f"{base_url}/{email_encoded}"
    params = {"token": "22548|PVsusDzEZnuek7rPOVOsPZCmk1hFXUbK"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['valid_format'] and data['valid_mx'] and not data['disposable']:
            return True
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Erro", err)
    return False


#função:validação externa de CPF
#função:validação externa de CPF
def validar_cpf(cpf):
    url = "https://api.invertexto.com/v1/validator"

    params = {
        "token": "22548|PVsusDzEZnuek7rPOVOsPZCmk1hFXUbK",
        "value": cpf["cpf_cnpj"]
    }

    try:
        response = requests.get(url, params = params)
        response.raise_for_status()

        data = response.json()
        if data['valid'] and data['formatted']:
            return True

    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Erro", err)
    return False


'''============> validarÇÕES BASE INTERNAS <============'''

#função:validação interna de nome
def validar_nome(nome):
    if len(nome["nome"]) < 3:
        return False

    for caractere in nome["nome"]:
        if caractere.isdigit():
            return False

    tem_espaco = False
    for caractere in nome["nome"]:
        if caractere.isspace():
            tem_espaco= True
            break
    if not tem_espaco:
        return False
    return True


#função:validação interna de quantidade
def validar_quantidade(quant):
    tem_letra = True
    for caractere in quant["quantidade"]:
        if caractere.isalpha():
            tem_letra = False
            break
    if not tem_letra:
        return False

    if int(quant["quantidade"]) < 0:
        return False

    if int(quant["quantidade"]) > 500:
        return False

    tem_numero = False
    for caractere in quant["quantidade"]:
        if caractere.isdigit():
            tem_numero = True
            break
    if not tem_numero:
        return False
    return True


#função:validação interna de preço
def validar_preco(preco):

    #Mínimo de quatro digitos
    if int(preco["valor"]) < 4:
        return False

    #Precisa conter números
    tem_numero = False
    for caractere in preco["valor"]:
        if caractere.isdigit():
            tem_numero = True
            break
    if not tem_numero:
        return False
    
    for caractere in preco["valor"]:
        if caractere.isalpha():
            return False
    
    return True


#função:validação interna de ID
def validar_id(id):
    #O id não pode conter letras
    tem_letra = False
    for caractere in id["id"]:
        if caractere.isalpha():
            tem_letra = True
            break
    if  tem_letra:
        return  False
    
    #É necessário conter apenas quatro digitos
    if not len(id["id"]) == 4:
        return False

    return True


#função:validação interna de senha
def validar_senha(senha):
    if len(senha["senha"]) < 8:
        return False

    tem_numero = False
    for caractere in senha["senha"]:
        if caractere.isdigit():
            tem_numero = True
            break
    if not tem_numero:
        return False

    tem_maiuscula = False
    for caractere in senha["senha"]:
        if caractere.isupper():
            tem_maiuscula = True
            break
    if not tem_maiuscula:
        return False

    tem_minuscula = False
    for caractere in senha["senha"]:
        if caractere.islower():
            tem_minuscula = True
            break
    if not tem_minuscula:
        return False

    return True


#função:validação interna de peso
def validar_peso(peso):
    tem_letra_peso = False
    for caractere in peso["peso"]:
        if caractere.isalpha():
            tem_letra_peso = True
            break
    if tem_letra_peso:
        return False
    
    if int(peso["peso"]) < 1:
        return False

    return True


#função:validação interna de data
def validar_data(dados_data):
    tem_letra_data = False
    for caractere in dados_data["data"]:
        if caractere.isalpha():
            tem_letra_data = True
            break
    if tem_letra_data:
        return False

    if not len(dados_data["data"]) == 6:
        return False
    
    return True


#função:validação de prateleira
def validar_prateleira(prateleira):
    tem_maiuscula = False
    for caractere in prateleira["prateleira"]:
        if caractere.isupper():
            tem_maiuscula = True
            break
    if not tem_maiuscula:
        return {"validar": False, "mensagem": "A prateleira deve conter pelo menos uma letra maiúscula."}
    
    if prateleira["prateleira"] != "A" or "B" or "C" or "D" or "E" or "F":
        return False
    return True


'''============> validarÇÕES ENDPOINTS <============'''


#função:validação de empilhadeira de saída e entrada 
def validar_empilhadeira(dados_empilhadeira):
    tem_letra = False
    for caractere in (dados_empilhadeira["codigo"]):
        if caractere.isalpha():
            tem_letra = True
            break
    if tem_letra:
        return False
    
    if not len(dados_empilhadeira["codigo"]) == 7:
        return False

    dados = validar_data(dados_empilhadeira)
    if dados:
        return True
    return False


#função:validação de funcionário
def validar_funcionario(funcionario):
    dados = validar_nome(funcionario)
    if dados:
        dados = validar_senha(funcionario)
        if dados:
            dados = validar_cpf(funcionario)
            if dados:
                dados = validar_email(funcionario)
                if dados:
                    dados = validar_cep(funcionario)
                    if dados:
                        return True
    return False


#função:validação de fornecedor
def validar_fornecedor(dados_fornecedor):

    #validar nome
    dados = validar_nome(dados_fornecedor)

    if dados:
        #validar email
        dados = validar_email(dados_fornecedor)

        if dados:
            #validar CEP
            dados = validar_cep(dados_fornecedor)
            
            if dados:
                return True
    return False


#função:validação de cliente
def validar_cliente(dados_cliente):

    #validar nome
    
    dados = validar_email(dados_cliente)
    

    if dados:
        #validar CPF
        print("email")
        dados = validar_senha(dados_cliente)
        

        if dados:
                #validar senha
            print("senha")
            dados = validar_nome(dados_cliente)

            if dados:
                #validar email
                print("nome")
                dados = validar_cpf(dados_cliente)

                if dados:
                #validar cep
                    print("cpf")
                    dados = validar_cep(dados_cliente)

                    if dados:
                        print("cep")
                        return True
    return False


#função:validação de setor de montagem
def validar_setormontagem(setor):
    dados = validar_empilhadeira(setor)
    if dados:
        dados = validar_quantidade(setor)
        if dados:
            return True
    return False


#função:validação de produto
def validar_produto(dados_produto):
    #validar nome
    if len(dados["nome"]) <= 0:
        return False

    #validar peso
    dados = validar_peso(dados_produto)
    if dados:
        #validar quantidade
        dados = validar_quantidade(dados_produto)
        if dados:
            return True
    return False

#função:validação de pedido de entrada
def validar_pedido_entrada(pedido_entrada):
    dados = validar_nome(pedido_entrada)
    if dados:
        dados = validar_quantidade(pedido_entrada)
        if dados:
            return True
    return False


#função:validação de pagamento de entrada e saída
def validar_pagamento(pagamento_entrada_saida):
    dados = validar_nome(pagamento_entrada_saida)
    if dados:
        dados = validar_quantidade(pagamento_entrada_saida)
        if dados:
            dados = validar_preco(pagamento_entrada_saida)
            if dados:
                return True
    return False


#função:validação de rota de saída
def validar_rota_saida(rota_saida):
    dados = validar_empilhadeira(rota_saida)
    if dados:
        dados = validar_quantidade(rota_saida)
        if dados:
            dados = validar_peso(rota_saida)
            if dados:
                dados = validar_prateleira(rota_saida)
                return True
    return False


#função:validação de lista de saída e entrada
def validar_lista(lista_saida_entrada):
    dados = validar_nome(lista_saida_entrada)
    if dados:
        dados = validar_quantidade(lista_saida_entrada)
        if dados:
            dados = validar_preco(lista_saida_entrada)
            if dados:
                dados = validar_peso
                return True
    return False


#função:validação de pedido de saída
def validar_pedido_saida(dados_pedido_saida):
    dados = validar_quantidade(dados_pedido_saida)
    if dados:
        return True
    return False


#função:validação de rota de entrada
def validar_rota_entrada(rota):

    #validação do campo "data"
    dados = validar_data(rota)

    if dados:
        #validação quantidade
        dados = validar_quantidade(rota)

        if dados:
            return True
    return False


#função:validação de estoque
def validar_estoque(dados_estoque):
    #validar quantidade
    dados = validar_quantidade(dados_estoque)

    if dados:
        dados = validar_id(dados_estoque)

        if dados:
            return True
    return False


def validar_uso(dados_uso):
    return