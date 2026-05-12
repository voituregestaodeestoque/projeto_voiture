#atualizado por clarinha 07/05 às 11h04

import urllib.parse
import datetime
import requests

#Validações revisadas pela Júlia em 30/04/2026
#ultimas atualizações dia 07/05/2026 às 8

class Validator:     

    #Validações não utilizadas por enquanto
    @staticmethod
    def required(value, field_name):
        if value is None or str(value).strip() == "":
            return{"valida":False, "mensagem":f"o campo {field_name} é obrigatório"}
        return {"valida": True}

    @staticmethod
    def non_negative(value, field_name):
        try:
            if float(value) < 0:
                return f"O campo {field_name} não pode ser negativo."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None

    @staticmethod
    def positive(value, field_name):
        try:
            if int(value) <= 0:
                return f"O campo {field_name} deve ser maior que zero."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None


    '''============> VALIDAÇÕES BASE EXTERNAS <============'''

    #função:validação externa de CEP
    @staticmethod
    def validar_cep(value, field_name):

        #Não pode ter letras
        for caractere in (value):
            if not(caractere.isdigit()):
                return {"valida":False,"mensagem":f"O campo {field_name} só pode ter números"}

        #Limite de 8 dígitos
        if  not len(value) == 8:
            return f"O campo {field_name} não suporta essa quantidade de caracteres"
        base_url = "https://api.invertexto.com/v1/cep"
        cep_encoded = urllib.parse.quote(value)
        url = f"{base_url}/{cep_encoded}"
        params = {"token":"22590|VRlqZZZ2IlPzK682Q8mjVW6n8SAwLWFO"}
        try:
            response = requests.get(url,params=params)
            response.raise_for_status()
            retorno_cep = response.json()
            if retorno_cep:
                return {"valida":True}
        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:",errh)
        except requests.exceptions.ConnectionError as errc:
            print("Erro de conexão:",errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:",errt)
        except requests.exceptions.RequestException as err:
            print("Erro:", err)
        return {"valida":False, "mensagem":"CEP inválido"}


    #função:validação externa de email
    @staticmethod
    def validar_email(value,field_name):
        base_url = "https://api.invertexto.com/v1/email-validator"
        email_encoded = urllib.parse.quote(value)
        url = f"{base_url}/{email_encoded}"
        params = {"token": "22548|PVsusDzEZnuek7rPOVOsPZCmk1hFXUbK"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data['valid_format'] and data['valid_mx'] and not data['disposable']:
                return {"valida":True}
        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Erro de conexão", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:", errt)
        except requests.exceptions.RequestException as err:
            print("Erro", err)
        return{"valida": False,"mensagem":"Email inválido"}


    #função:validação externa de CPF/CNPJ
    @staticmethod
    def validar_cpf_cnpj(value, field_name):
        url = "https://api.invertexto.com/v1/validator"

        params = {
            "token": "22548|PVsusDzEZnuek7rPOVOsPZCmk1hFXUbK",
            "value": (value)
        }

        try:
            response = requests.get(url, params = params)
            response.raise_for_status()

            data = response.json()
            if data['valid'] and data['formatted']:
                return{"valida":True}

        except requests.exceptions.HTTPError as errh:
            print("Erro HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Erro de conexão", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout:", errt)
        except requests.exceptions.RequestException as err:
            print("Erro", err)
        return {"valida":False,"mensagem":"CPF/CNPJ inválido"}


    '''============> Validações BASE INTERNAS <============'''

    #Função:validação de telefone
    @staticmethod
    def validar_telefone(value, field_name):

        #Não pode ter letras
        tem_letra = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra = True
                break
        if tem_letra:
            return {"valida":False, "mensagem":f"O campo {field_name} não pode haver letras"}
        
        return {"valida":True}

    #função:validação interna de nome
    @staticmethod
    def validar_nome(value, field_name):

        #Nomes devem ter mais de 3 letras
        if len(value) < 3:
            return {"valida":False, "mensagem":f"{field_name}deve ter no mínimo 3 letras"}

        #Nomes não podem ter números
        for caractere in (value):
            if caractere.isdigit():
                return{"valida":False, "mensagem":f"O campo {field_name} não pode haver números"}

        #O nome deve estar completo (nome e sobrenome)
        tem_espaco = False
        for caractere in (value):
            if caractere.isspace():
                tem_espaco= True
                break
        if tem_espaco == False:
            return{"valida":False,"mensagem":f"O campo {field_name} não pode ter somente o primeiro nome."}
        return {"valida":True}


    #função:validação interna de quantidade
    @staticmethod
    def validar_quantidade(value, field_name):

        #Não pode conter letras
        tem_letra = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra = True
                break
        if tem_letra:
            return{"valida":False, "mensagem":f"O campo {field_name} não pode haver letras"}

        return {"valida":True}
        


    #função:validação interna de preço
    @staticmethod
    def validar_preco(value, field_name):

        #Não pode ter letras
        tem_letra = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra = True
                break

        if tem_letra:
            return{"valida":False, "mensagem":f"O campo {field_name} não pode haver letras"}
        
        return {"valida":True}


    #função: validação interna de ddi e ddd
    @staticmethod
    def validar_ddi_ddd(value, field_name):

        #Máximo de 5 dígitos
        if len(value) > 5:
            return{"valida":False, "mensagem": f"Quantidade de caracteres em {field_name} é inválida"}
        
        #Não pode ter letras
        tem_letra = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra = True
                break
        if tem_letra:
            return{"valida":False, "mensagem": f"O campo {field_name} não pode haver letras"}
        
        return {"valida":True}

    #função:validação interna de senha
    @staticmethod
    def validar_senha(value, field_name):

        #Não pode ter mais de 200 caracteres
        if len(value) > 200:
            return{"valida":False,"mensagem":f"O campo {field_name} não pode ter mais de 200 caracteres"}

        #Deve ter números
        tem_numero = False
        for caractere in (value):
            if caractere.isdigit():
                tem_numero = True
                break
        if not tem_numero:
            return {"valida":False,"mensagem":f"O campo {field_name} deve ter números"}

        #Deve ter maiúsculas
        tem_maiuscula = False
        for caractere in (value):
            if caractere.isupper():
                tem_maiuscula = True
                break
        if not tem_maiuscula:
            return{"valida":False,"mensagem":f"O campo {field_name} deve ter letras maiúsculas"}

        #Deve ter minúsculas
        tem_minuscula = False
        for caractere in (value):
            if caractere.islower():
                tem_minuscula = True
                break
        if not tem_minuscula:
            return{"valida":False,"mensagem":f"O campo {field_name} deve ter uma letra minúscula"}

        return {"valida":True}


    #função:validação interna de peso
    @staticmethod
    def validar_peso(value, field_name):

        #Não deve ter letras
        tem_letra = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra = True
                break
        if tem_letra:
            return {"valida":False,"mensagem":f"O campo {field_name} não pode haver letras"}
        
        #Não pode ter valores negativos
        if int(value) <= 0:
            return {"valida":False,"mensagem":f"O campo {field_name} não aceita valores negativos"}

        return {"valida":True}

    #Validações adicionadas dia 05/05/2026 ryan ribeiro

    #atualizações e finalizações no dia 07/05/2026
    def validar_chassi(value, field_name):
        #Não pode ter mais de 20 caracteres
        if len(value) > 20:
            return{"valida":False,"mensagem":f"O campo {field_name} não pode ter mais de 20 caracteres"}
        return {"valida":True}
     
    def validar_modelo(value, field_name):
        #
        if len(value) > 20:
            return{"valida":False,"mensagem":f"O campo {field_name} não pode ter mais de 20 caracteres"}
        return {"valida":True}

    def validar_marca(value, field_name):
        #Não pode ter mais de 20 caracteres
        if len(value) > 20:
            return{"valida":False,"mensagem":f"O campo {field_name} não pode ter mais de 20 caracteres"}
        return {"valida":True}
    
    def validar_status(value, field_name):
        #Não pode ter mais de 10 caracteres
        if len(value) > 10:
            return{"valida":False,"mensagem":f"O campo {field_name} não pode ter mais de 10 caracteres"}
    
    @staticmethod
    def validar_localizacao(value, field_name):
        for caractere in (value):
            if caractere.isdigit():
                return{"valida":False, "mensagem":f"O campo {field_name} não pode haver números"}

        tem_maiuscula = False
        for caractere in (value):
            if caractere.isupper():
                tem_maiuscula = True
                break
        if not tem_maiuscula:
            return{"valida":False,"mensagem":f"O campo {field_name} deve ter apenas letras maiúsculas"}

        tem_minuscula = True
        for caractere in (value):
            if caractere.islower():
                tem_minuscula = False
                break
        if tem_minuscula:
            return{"valida": False, "mensagem":f"O campo {field_name} não deve ter letras minúsculas"}

        return{"valida":True}

    @staticmethod
    def validar_descricao(value, field_name):
        #Não pode ter mais de 700 caracteres
        if len(value) > 700:
            return{"valida":False,"mensagem":f"O campo {field_name} atingiu o limite de caracteres"}

        return{"valida":True}

    @staticmethod
    def validar_cargo(value, field_name):
        #Não pode ter mais de 700 caracteres
        if len(value) > 700:
            return{"valida":False,"mensagem":f"O campo {field_name} atingiu o limite de caracteres"}

        return{"valida":True}
    


        


        





