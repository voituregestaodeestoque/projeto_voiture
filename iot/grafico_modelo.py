from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)

CORS(app)


# =========================================================
# CONFIGURAÇÃO DO BANCO
# =========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "voiture_estoque"
}


def conectar():

    return mysql.connector.connect(
        **DB_CONFIG
    )


# =========================================================
# DISTÂNCIA HC-SR04
# =========================================================

@app.route("/api/distancia")
def distancia():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            device_id,
            distancia,
            data_hora
        FROM leituras
        WHERE sensor = 'HC-SR04'
        ORDER BY data_hora DESC
        LIMIT 100
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    dados.reverse()

    for item in dados:

        item["distancia"] = float(
            item["distancia"]
        ) if item["distancia"] is not None else None

        item["data_hora"] = item[
            "data_hora"
        ].strftime("%Y-%m-%d %H:%M:%S")


    return jsonify(dados)


# =========================================================
# RFID
# =========================================================

@app.route("/api/rfid")
def rfid():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            device_id,
            rfid_uid,
            data_hora
        FROM leituras
        WHERE sensor = 'MFRC522'
          AND rfid_uid IS NOT NULL
        ORDER BY data_hora DESC
        LIMIT 50
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    dados.reverse()


    # -----------------------------------------------------
    # Regra DIDÁTICA de entrada / saída
    # -----------------------------------------------------

    estados = {}

    for item in dados:

        uid = item["rfid_uid"]

        if uid not in estados:

            estados[uid] = "ENTRADA"

        else:

            if estados[uid] == "ENTRADA":

                estados[uid] = "SAIDA"

            else:

                estados[uid] = "ENTRADA"


        item["movimento"] = estados[uid]

        item["data_hora"] = item[
            "data_hora"
        ].strftime("%Y-%m-%d %H:%M:%S")


        # Produto fictício associado ao UID
        item["produto"] = (
            "Produto RFID " + uid[-4:]
        )


    return jsonify(dados)


# =========================================================
# RESUMO DO DASHBOARD
# =========================================================

@app.route("/api/resumo")
def resumo():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    # Última leitura RFID

    cursor.execute("""
        SELECT
            rfid_uid,
            data_hora
        FROM leituras
        WHERE sensor = 'MFRC522'
          AND rfid_uid IS NOT NULL
        ORDER BY data_hora DESC
        LIMIT 1
    """)

    ultimo_rfid = cursor.fetchone()


    # Quantidade RFID

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM leituras
        WHERE sensor = 'MFRC522'
          AND rfid_uid IS NOT NULL
    """)

    total_rfid = cursor.fetchone()


    cursor.close()
    conexao.close()


    leitor_ativo = False


    if ultimo_rfid:

        agora = datetime.now()

        diferenca = (
            agora -
            ultimo_rfid["data_hora"]
        ).total_seconds()


        # Considera leitor ativo
        # se houve leitura nos últimos 60 segundos

        leitor_ativo = diferenca <= 60


    return jsonify({

        "rfid_total":
            total_rfid["total"],

        "rfid_ultimo":
            ultimo_rfid["rfid_uid"]
            if ultimo_rfid
            else None,

        "leitor_ativo":
            leitor_ativo

    })


# =========================================================
# STATUS
# =========================================================

@app.route("/api/status")
def status():

    return jsonify({

        "api": "online",

        "banco": "voiture_estoque",

        "status": "OK"

    })


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )