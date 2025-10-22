import json
from src.fileDispositivo import Dispositivo

class ComunicadorSensores:
    def __init__(self):
        self.nombreArchivo = "data/DatosSensores.json"

        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
        self.topics = config["TOPICSsensores"]
        
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
        Dispositivo.clearConsole()
        print("Ctrl+C para salir")
        print(f"Mensaje recibido en el tema '{msg.topic}':")
        print(msg.payload.decode("utf-8"))

        try:
            # Decodificar y convertir el mensaje de JSON a diccionario
            payload = json.loads(msg.payload.decode("utf-8"))
            print(json.dumps(payload, indent=4))  # Mostrar el mensaje formateado

            Dispositivo.guardarDatos(payload, self.nombreArchivo)

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")