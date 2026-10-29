import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from mysql.connector import pooling

class Database:
    @staticmethod
    def connect():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            raise Exception(f"Falha na conexão com o banco de dados: {e}")




#IOT

# =====================================================
# POOL DE CONEXOES
# =====================================================

pool = pooling.MySQLConnectionPool(
    pool_name="pool_sensores",
    pool_size=5,
    **DB_CONFIG
)

# =====================================================
# SALVAR LEITURA
# =====================================================

def salvar_leitura(
    device_id,
    sensor,
    distancia=None,
    rfid_uid=None
):

    conn = None
    cursor = None

    try:

        conn = pool.get_connection()

        cursor = conn.cursor()

        sql = """
            INSERT INTO leituras
            (
                device_id,
                sensor,
                distancia,
                rfid_uid
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        valores = (
            device_id,
            sensor,
            distancia,
            rfid_uid
        )

        cursor.execute(
            sql,
            valores
        )

        conn.commit()

        print(
            f"Leitura salva: "
            f"{device_id} | {sensor}"
        )

        return True


    except Exception as erro:

        print(
            "Erro ao salvar leitura:"
        )

        print(erro)

        return False


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# =====================================================
# LISTAR LEITURAS
# =====================================================

def listar_leituras(
    device_id=None,
    sensor=None,
    limite=100
):

    conn = None
    cursor = None

    try:

        # ---------------------------------------------
        # Protecao simples para o LIMIT
        # ---------------------------------------------

        limite = int(limite)

        if limite < 1:
            limite = 1

        if limite > 1000:
            limite = 1000


        conn = pool.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )


        # ---------------------------------------------
        # MONTA A CONSULTA
        # ---------------------------------------------

        sql = """
            SELECT
                id,
                device_id,
                sensor,
                distancia,
                rfid_uid,
                data_hora

            FROM leituras
        """

        filtros = []

        valores = []


        # ---------------------------------------------
        # FILTRO DEVICE
        # ---------------------------------------------

        if device_id:

            filtros.append(
                "device_id = %s"
            )

            valores.append(
                device_id
            )


        # ---------------------------------------------
        # FILTRO SENSOR
        # ---------------------------------------------

        if sensor:

            filtros.append(
                "sensor = %s"
            )

            valores.append(
                sensor
            )


        # ---------------------------------------------
        # WHERE
        # ---------------------------------------------

        if filtros:

            sql += " WHERE "

            sql += " AND ".join(
                filtros
            )


        # ---------------------------------------------
        # ORDENACAO E LIMITE
        # ---------------------------------------------

        sql += """
            ORDER BY data_hora DESC, id DESC
            LIMIT %s
        """

        valores.append(
            limite
        )


        cursor.execute(
            sql,
            tuple(valores)
        )

        resultado = cursor.fetchall()

        return resultado


    except Exception as erro:

        print(
            "Erro ao listar leituras:"
        )

        print(erro)

        return []


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# =====================================================
# TESTE DIRETO DO ARQUIVO
# =====================================================
#
# Esta parte só roda quando executamos:
#
# python database.py
#
# Quando o FastAPI importar este arquivo,
# ela NÃO será executada.
#

if __name__ == "__main__":

    print()
    print("================================")
    print("   TESTE DATABASE - SENAI")
    print("================================")

    print()
    print("Testando conexao com MySQL...")


    # =================================================
    # TESTE HC-SR04
    # =================================================

    print()
    print("Inserindo teste HC-SR04...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="HC-SR04",
        distancia=38.50
    )


    # =================================================
    # TESTE MFRC522
    # =================================================

    print()
    print("Inserindo teste MFRC522...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="MFRC522",
        rfid_uid="TESTE-01-02-03"
    )


    # =================================================
    # CONSULTAR
    # =================================================

    print()
    print("================================")
    print("LEITURAS GRAVADAS")
    print("================================")

    leituras = listar_leituras(
        device_id="esp32-teste",
        limite=10
    )


    for leitura in leituras:

        print()
        print(leitura)


    print()
    print("================================")
    print("TESTE FINALIZADO")
    print("================================")
