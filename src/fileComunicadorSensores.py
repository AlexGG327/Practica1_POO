import json
import paho.mqtt.client as mqtt

from fileRefresh import clearConsole
from fileGuardado import guardarDatosSensores

nombreArchivo = "DatosSensores.json"

# Configuración del cliente MQTT
  # Temas a los que se suscribirá el cliente

class ComunicadorSensores:
    def __init__(self, broker, port, topics):
        self.broker = broker
        self.port = port
        self.topics = topics
        
    # Callback cuando se establece la conexión con el broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            for topic in self.topics:
                client.subscribe(topic)
                print(f"Suscrito al tema '{topic}'")
        else:
            print(f"Error de conexión, código: {rc}")

    # Callback cuando se recibe un mensaje en los temas suscritos
    def on_message(self, client, userdata, msg):
        clearConsole()
        print("Ctrl+C para salir")
        print(f"Mensaje recibido en el tema '{msg.topic}':")
        print(msg.payload.decode("utf-8"))

        try:
            # Decodificar y convertir el mensaje de JSON a diccionario
            payload = json.loads(msg.payload.decode("utf-8"))
            print(json.dumps(payload, indent=4))  # Mostrar el mensaje formateado

            guardarDatosSensores(payload, nombreArchivo)
            #print(f"Datos guardados en {nombreArchivo}")

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")

"""
BROKER = "broker.emqx.io"  # Cambia esto por tu broker MQTT
PORT = 1883  # Puerto del broker MQTT
TOPICS = ["sensor/data/sen55", "sensor/data/gas_sensor"]

ordenadorSensores = ComunicadorSensores(BROKER, PORT, TOPICS)

# Crear un cliente MQTT
client = mqtt.Client()

# Asignar las funciones de callback
client.on_connect = ordenadorSensores.on_connect
client.on_message = ordenadorSensores.on_message

# Conectar al broker MQTT
client.connect(BROKER, PORT, 60)

# Bucle principal para mantener la conexión y escuchar mensajes
print("Esperando mensajes... Presiona Ctrl+C para salir")
try:
    client.loop_forever()  # Mantener el cliente en ejecución
except KeyboardInterrupt:
    print("Desconectando del broker...")
    client.disconnect()
"""