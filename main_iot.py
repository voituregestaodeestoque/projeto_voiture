"""
main.py
Projeto IoT SENAI - ESP32 MULTISSENSOR

Sensores:
- DHT11
- HC-SR04
- MFRC522

Arquitetura:
ESP32
  -> HiveMQ Cloud (MQTT)
  -> FastAPI
  -> MySQL

Todos os sensores habilitados.
"""

import network
import time
import ujson
import dht

from machine import Pin, SPI
from umqtt.simple import MQTTClient
from mfrc522 import MFRC522


# =====================================================
# 1. ESCOLHA DOS SENSORES
# =====================================================

USAR_ULTRASSONICO = True
USAR_RFID = True


# =====================================================
# 2. IDENTIFICACAO DO ESP32
# =====================================================

DEVICE_ID = "esp32-voiture"


# =====================================================
# 3. WIFI
# =====================================================

WIFI_SSID = "SENAI-IOT"
WIFI_PASSWORD = "12345678"


# =====================================================
# 4. MQTT - HIVEMQ CLOUD
# =====================================================

MQTT_BROKER = (
    "b1600c60a35c4520b32b9507d0b47b02"
    ".s1.eu.hivemq.cloud"
)

MQTT_PORT = 8883

MQTT_USER = "IOT-SENAI"
MQTT_PASSWORD = "12345678"

MQTT_CLIENT_ID = "esp32-sensores-01"

MQTT_TOPIC = b"sensores/leitura/voiture"


# =====================================================
# 6. CONFIGURACAO HC-SR04
# =====================================================

if USAR_ULTRASSONICO:

    trig = Pin(
        25,
        Pin.OUT
    )

    echo = Pin(
        26,
        Pin.IN
    )

    trig.value(0)


# =====================================================
# 7. CONFIGURACAO MFRC522
# =====================================================

#
#| SDA  | GPIO 5  |
#| SCK  | GPIO 18 |
#| MOSI | GPIO 23 |
#| MISO | GPIO 19 |
#| RST  | GPIO 22 |
#| 3.3V | 3V3     |
#| GND  | GND     |

if USAR_RFID:

    print()
    print("Configurando MFRC522...")

    spi = SPI(
        2,
        baudrate=2500000,
        polarity=0,
        phase=0,
        sck=Pin(18),
        mosi=Pin(23),
        miso=Pin(19)
    )

    rfid = MFRC522(
        spi=spi,
        gpioRst=22,
        gpioCs=5
    )

    print("MFRC522 configurado.")


# =====================================================
# 8. CONTROLE DO RFID
# =====================================================

ultimo_uid = None

leituras_sem_cartao = 0


# =====================================================
# 9. CONECTAR AO WIFI
# =====================================================

def conectar_wifi():

    print()
    print("================================")
    print("CONECTANDO AO WIFI")
    print("================================")

    wifi = network.WLAN(
        network.STA_IF
    )

    wifi.active(True)

    if not wifi.isconnected():

        print("Conectando ao Wi-Fi...")

        wifi.connect(
            WIFI_SSID,
            WIFI_PASSWORD
        )

        contador = 0

        while not wifi.isconnected():

            print(".", end="")

            time.sleep(1)

            contador += 1

            if contador >= 30:

                print()
                print("ERRO: Wi-Fi nao conectou.")

                return False


    print()
    print("Wi-Fi conectado com sucesso!")

    configuracao = wifi.ifconfig()

    print()
    print("IP:     ", configuracao[0])
    print("Mascara:", configuracao[1])
    print("Gateway:", configuracao[2])
    print("DNS:    ", configuracao[3])

    return True


# =====================================================
# 10. CONECTAR AO MQTT
# =====================================================

def conectar_mqtt():

    print()
    print("================================")
    print("CONECTANDO AO MQTT")
    print("================================")

    print("Broker:")
    print(MQTT_BROKER)

    print()
    print("Porta:", MQTT_PORT)
    print("Usuario:", MQTT_USER)
    print("Client ID:", MQTT_CLIENT_ID)

    print()
    print("TLS: ATIVADO")
    print("SNI: ATIVADO")

    print()
    print("Conectando...")


    try:

        client = MQTTClient(
            MQTT_CLIENT_ID,
            MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True,
            ssl_params={
                "server_hostname": MQTT_BROKER
            }
        )

        client.connect()

        print()
        print("================================")
        print("MQTT CONECTADO COM SUCESSO!")
        print("================================")

        return client


    except Exception as erro:

        print()
        print("================================")
        print("ERRO NA CONEXAO MQTT")
        print("================================")

        print("Tipo:")
        print(type(erro))

        print()
        print("Erro:")
        print(erro)

        return None


# =====================================================
# 11. PUBLICAR MQTT
# =====================================================

def publicar(client, dados):

    try:

        mensagem = ujson.dumps(
            dados
        )

        print()
        print("Publicando MQTT...")

        print("Topico:")
        print(MQTT_TOPIC)

        print()
        print("Mensagem:")
        print(mensagem)


        client.publish(
            MQTT_TOPIC,
            mensagem
        )


        print()
        print("MQTT enviado com sucesso!")

        return True


    except Exception as erro:
        print()
        print("ERRO AO PUBLICAR MQTT")

        print("Tipo:")
        print(type(erro))

        print("Erro:")
        print(erro)

        return False


# =====================================================
# 12. INICIALIZACAO DO DHT11
# =====================================================

# =====================================================
# 13. LEITURA DO DHT11
# =====================================================

# =====================================================
# 14. LEITURA DO HC-SR04
# =====================================================

def ler_ultrassonico(client):

    try:

        # ---------------------------------------------
        # Pulso TRIGGER
        # ---------------------------------------------

        trig.value(0)

        time.sleep_us(2)

        trig.value(1)

        time.sleep_us(10)

        trig.value(0)


        # ---------------------------------------------
        # Espera inicio do ECHO
        # ---------------------------------------------

        timeout = time.ticks_us()


        while echo.value() == 0:

            if time.ticks_diff(
                time.ticks_us(),
                timeout
            ) > 30000:

                raise Exception(
                    "Timeout esperando inicio do ECHO"
                )


        inicio = time.ticks_us()


        # ---------------------------------------------
        # Espera final do ECHO
        # ---------------------------------------------

        timeout = time.ticks_us()


        while echo.value() == 1:

            if time.ticks_diff(
                time.ticks_us(),
                timeout
            ) > 30000:

                raise Exception(
                    "Timeout esperando final do ECHO"
                )


        fim = time.ticks_us()


        # ---------------------------------------------
        # Calcula duracao
        # ---------------------------------------------

        duracao = time.ticks_diff(
            fim,
            inicio
        )


        # ---------------------------------------------
        # Calcula distancia
        # ---------------------------------------------

        distancia = (
            duracao * 0.0343
        ) / 2


        distancia = round(
            distancia,
            2
        )


        print()
        print("--------------------------------")
        print("HC-SR04")
        print("--------------------------------")

        print(
            "Distancia:",
            distancia,
            "cm"
        )


        dados = {

            "device_id": DEVICE_ID,

            "sensor": "HC-SR04",

            "distancia": distancia
        }


        publicar(
            client,
            dados
        )


    except Exception as erro:

        print()
        print("Aviso: leitura HC-SR04 nao realizada.")

        print("Erro:")
        print(erro)


# =====================================================
# 15. CONVERTER UID RFID
# =====================================================

def converter_uid(uid):

    texto = ""

    for numero in uid:

        if texto != "":

            texto += "-"

        texto += "{:02X}".format(
            numero
        )

    return texto


# =====================================================
# 16. LEITURA RFID
# =====================================================

def ler_rfid(client):

    global ultimo_uid
    global leituras_sem_cartao


    try:

        # ---------------------------------------------
        # PROCURA CARTAO
        # ---------------------------------------------

        status, tag_type = rfid.request(
            rfid.REQIDL
        )


        # ---------------------------------------------
        # NENHUM CARTAO
        # ---------------------------------------------

        if status != rfid.OK:

            if ultimo_uid is not None:

                leituras_sem_cartao += 1


                # Confirma que o cartão foi retirado.

                if leituras_sem_cartao >= 3:

                    print()
                    print("--------------------------------")
                    print("Cartao retirado.")
                    print("RFID liberado para nova leitura.")
                    print("--------------------------------")

                    ultimo_uid = None

                    leituras_sem_cartao = 0


            return


        # Cartão detectado

        leituras_sem_cartao = 0


        # ---------------------------------------------
        # LER UID
        # ---------------------------------------------

        status, uid = rfid.anticoll()


        if status != rfid.OK:

            return


        uid_texto = converter_uid(
            uid
        )


        # ---------------------------------------------
        # MESMO CARTAO
        # ---------------------------------------------

        if uid_texto == ultimo_uid:

            return


        # ---------------------------------------------
        # NOVO CARTAO
        # ---------------------------------------------

        print()
        print("--------------------------------")
        print("MFRC522")
        print("--------------------------------")

        print("Novo cartao detectado!")

        print()
        print("UID:")

        print(
            uid_texto
        )


        dados = {

            "device_id": DEVICE_ID,

            "sensor": "MFRC522",

            "rfid_uid": uid_texto
        }


        publicado = publicar(
            client,
            dados
        )


        if publicado:

            ultimo_uid = uid_texto

            print()
            print("Cartao registrado.")

            print(
                "Retire o cartao para"
            )

            print(
                "permitir nova leitura."
            )


    except Exception as erro:

        print()
        print("Aviso: falha na leitura RFID.")

        print("Erro:")
        print(erro)


# =====================================================
# 17. INICIO DO SISTEMA
# =====================================================

print()
print("================================")
print("     SISTEMA IoT - SENAI")
print("================================")

print()
print("ESP32 MULTISSENSOR")

print()
print("Sensores habilitados:")


print(
    "HC-SR04:",
    USAR_ULTRASSONICO
)

print(
    "MFRC522:",
    USAR_RFID
)

print()
print("================================")


# =====================================================
# 18. CONECTAR AO WIFI
# =====================================================

wifi_ok = conectar_wifi()


if not wifi_ok:

    print()
    print("Sistema interrompido.")
    print("Motivo: falha no Wi-Fi.")

    raise SystemExit


# =====================================================
# 19. CONECTAR AO MQTT
# =====================================================

client = conectar_mqtt()


if client is None:

    print()
    print("Sistema interrompido.")
    print("Motivo: falha no MQTT.")

    raise SystemExit


# =====================================================
# 20. INICIALIZAR DHT11
# =====================================================


# =====================================================
# 21. SISTEMA PRONTO
# =====================================================

print()
print("================================")
print("SISTEMA INICIALIZADO")
print("================================")

print("Wi-Fi: OK")
print("MQTT: OK")

print()
print("Sensores ativos:")

print("HC-SR04")
print("MFRC522")

print()
print("Iniciando monitoramento...")

print("================================")


# =====================================================
# 22. CONTROLE DE TEMPO
# =====================================================
#
# DHT11 e HC-SR04:
# leitura a cada 5 segundos.
#
# RFID:
# verificado continuamente.
#

ultima_leitura_sensores = time.ticks_ms()


# =====================================================
# 23. LOOP PRINCIPAL
# =====================================================

while True:

    agora = time.ticks_ms()


    # =================================================
    # DHT11 + HC-SR04
    # =================================================

    if time.ticks_diff(
        agora,
        ultima_leitura_sensores
    ) >= 5000:


        print()
        print("================================")
        print("NOVA RODADA DE LEITURAS")
        print("================================")



        # ---------------------------------------------
        # HC-SR04
        # ---------------------------------------------

        if USAR_ULTRASSONICO:

            ler_ultrassonico(
                client
            )


        ultima_leitura_sensores = agora


    # =================================================
    # RFID
    # =================================================

    if USAR_RFID:

        ler_rfid(
            client
        )


    # Pequena pausa para não sobrecarregar o ESP32

    time.sleep_ms(200)