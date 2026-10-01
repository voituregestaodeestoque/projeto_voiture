#importações de tudo que vai ser usado no arquivo
import os
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage
from flask import flash

load_dotenv() #carrega as informações do .env


class EmailService:#Serviço responsável por montar e enviar emails de contato da Voiture.
    #configurações do email voiture
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 465

    #executado automaticamente quando você cria um objeto
    def __init__(self):
        self.email_sistema = os.getenv("EMAIL_SISTEMA")
        self.email_senha = os.getenv("EMAIL_SENHA")
        self.email_empresa = os.getenv("EMAIL_EMPRESA")

    #Função responsável por montar a mensagem do email
    def _montar_mensagem(self, nome, email_cliente, cnpj):
        mensagem = EmailMessage()

        mensagem["Subject"] = "Novo contato - Voiture"
        mensagem["From"] = self.email_sistema
        mensagem["To"] = self.email_empresa
        mensagem["Reply-To"] = email_cliente

        mensagem.set_content(f"""
Olá!

Uma nova empresa entrou em contato através da Landing Page da Voiture.

Nome do representante: {nome}

Email de contato: {email_cliente}

CNPJ da empresa: {cnpj}

Entre em contato com o representante para marcar uma reunião.

Atenciosamente,

Sistema Voiture - Gestão de Estoque
""")

        return mensagem

    #Função responsável por montar a mensagem do email
    def _montar_mensagem_bloqueio(self, email_destino, funcionario_nome, funcionario_email):
        mensagem = EmailMessage()

        mensagem["Subject"] = "Funcionário bloqueado - Voiture"
        mensagem["From"] = self.email_sistema
        mensagem["To"] = email_destino

        mensagem.set_content(f"""
Olá!

O funcionário abaixo foi bloqueado após 3 tentativas de login incorretas:

Nome: {funcionario_nome}

Email: {funcionario_email}

Acesse o painel administrativo para desbloquear o acesso, caso necessário.

Atenciosamente,

Sistema Voiture - Gestão de Estoque
""")

        return mensagem

    #Função responsável por conectar de forma segura o email
    def _enviar(self, mensagem):
        #conecta no email
        with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT) as servidor:
            servidor.login(self.email_sistema, self.email_senha)
            servidor.send_message(mensagem)

    #Função responsável por enviar o email contato
    def enviar_email(self, nome, email_cliente, cnpj):
        try:
            mensagem = self._montar_mensagem(nome, email_cliente, cnpj)
            self._enviar(mensagem)

            return True

        except Exception as erro:

            return False

    #Função responsável por enviar o email de bloqueio
    def enviar_email_bloqueio(self, email_destino, funcionario_nome, funcionario_email):
        try:
            mensagem = self._montar_mensagem_bloqueio(email_destino, funcionario_nome, funcionario_email)
            self._enviar(mensagem)

            return True

        except Exception as erro:

            return False


# Uso:
# email_service = EmailService()
# email_service.enviar_email_bloqueio(email_admin, funcionario_nome, funcionario_email)