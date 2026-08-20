import os
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage
from flask import flash

load_dotenv()


class EmailService:
    """Serviço responsável por montar e enviar emails de contato da Voiture."""

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 465

    def __init__(self):
        self.email_sistema = os.getenv("EMAIL_SISTEMA")
        self.email_senha = os.getenv("EMAIL_SENHA")
        self.email_empresa = os.getenv("EMAIL_EMPRESA")

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

    def _enviar(self, mensagem):
        with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT) as servidor:
            servidor.login(self.email_sistema, self.email_senha)
            servidor.send_message(mensagem)

    def enviar_email(self, nome, email_cliente, cnpj):
        try:
            mensagem = self._montar_mensagem(nome, email_cliente, cnpj)
            self._enviar(mensagem)

            return True

        except Exception as erro:
            
            return False


# Uso:
# email_service = EmailService()
# email_service.enviar_email(nome, email_cliente, cnpj)