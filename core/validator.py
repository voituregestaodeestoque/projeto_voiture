import urllib.parse
import datetime

class Validator:
    @staticmethod
    def validar_telefone(value, field_name):
        tem_letra_peso = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra_peso = True
                break
        if tem_letra_peso:
            return f"O campo {field_name} não pode haver letras"
        
        return True

        

    @staticmethod
    def required(value, field_name):
        if value is None or str(value).strip() == "":
            return f"O campo {field_name} é obrigatório."
        return None

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


    '''============> validarÇÕES BASE EXTERNAS <============'''

    #função:validação externa de CEP
    '''@staticmethod
    def validar_cep(value, field_name):
        for caractere in (value):
            if not(caractere.isdigit()):
                return f"O campo {field_name} só pode haver números"
        if  not len(value) == 8:
            return f"O campo {field_name} deve possuir 8 números"
        base_url = "https://api.invertexto.com/v1/cep"
        cep_encoded = urllib.parse.quote(value)
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
    @staticmethod
    def validar_cpf(value, field_name):
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
'''

    '''============> validarÇÕES BASE INTERNAS <============'''

    #função:validação interna de nome
    @staticmethod
    def validar_nome(value, field_name):
        if len(value) < 3:
            return f"O campo {field_name} não deve ter menos de 3 letras"

        for caractere in (value):
            if caractere.isdigit():
                return f"O campo {field_name} não pode haver números"

        tem_espaco = False
        for caractere in (value):
            if caractere.isspace():
                tem_espaco= True
                break
        if tem_espaco == True:
            return f"O campo {field_name} não pode haver espaço"
        return True


    #função:validação interna de quantidade
    @staticmethod
    def validar_quantidade(value, field_name):
        tem_letra = True
        for caractere in (value):
            if caractere.isalpha():
                tem_letra = False
                break
        if not tem_letra:
            return f"O campo {field_name} não pode haver letras"

        if int(value) < 0:
            return f"O campo {field_name} não deve ser negativo "

        if int(value) > 500:
            return f"O campo {field_name} não pode ser mais de 500"

        tem_numero = False
        for caractere in (value):
            if caractere.isdigit():
                tem_numero = True
                break
        if not tem_numero:
            return f"O campo {field_name} deve ser apenas números"
        return True


    #função:validação interna de preço
    @staticmethod
    def validar_preco(value, field_name):

        #Mínimo de quatro digitos
        if len(value) < 4:
            return f"O campo {field_name} precisa ter pelo menos 4 dígitos"

        #Precisa conter números
        tem_numero = False
        for caractere in (value):
            if caractere.isdigit():
                tem_numero = True
                break
        if not tem_numero:
            return f"O campo {field_name} deve ser apenas números"
        
        for caractere in (value):
            if caractere.isalpha():
                return f"O campo {field_name} não pode haver letras"
        
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
    
    @staticmethod
    def validar_ddi_ddd(value, field_name):
        if not len(value) == 2:
            return f"O campo {field_name} deve possuir apenas 2 caracteres"
        
        tem_letra_peso = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra_peso = True
                break
        if tem_letra_peso:
            return f"O campo {field_name} não pode haver letras"
        
        return True


    #função:validação interna de senha
    @staticmethod
    def validar_senha(value, field_name):
        if len(value) > 200:
            return f"O campo {field_name} não pode haver mais de 200 caracteres"

        tem_numero = False
        for caractere in (value):
            if caractere.isdigit():
                tem_numero = True
                break
        if not tem_numero:
            return f"O campo {field_name} deve ter números"

        tem_maiuscula = False
        for caractere in (value):
            if caractere.isupper():
                tem_maiuscula = True
                break
        if not tem_maiuscula:
            return f"O campo {field_name} deve ter uma letra maiúscula"

        tem_minuscula = False
        for caractere in (value):
            if caractere.islower():
                tem_minuscula = True
                break
        if not tem_minuscula:
            return f"O campo {field_name} deve ter uma letra minúscula"

        return True


    #função:validação interna de peso
    @staticmethod
    def validar_peso(value, field_name):
        tem_letra_peso = False
        for caractere in (value):
            if caractere.isalpha():
                tem_letra_peso = True
                break
        if tem_letra_peso:
            return f"O campo {field_name} não pode haver letras"
        
        if int(value) <= 0:
            return f"O campo {field_name} deve ser maior que 0"

        return True


    #função:validação interna de data
    @staticmethod
    def validar_data(value, field_name):
        value=datetime.datetimenow
        
        return True


    #função:validação de prateleira
    @staticmethod
    def validar_prateleira(value, field_name):
        tem_maiuscula = False
        for caractere in value:
            if caractere.isupper():
                tem_maiuscula = True
                break
        if not tem_maiuscula:
            return f"A prateleira deve conter pelo menos uma letra maiúscula."
        
        if value != "A" or "B" or "C" or "D" or "E" or "F":
            return f"A prateleira deve conter pelo menos uma letra maiúscula."
        return True
