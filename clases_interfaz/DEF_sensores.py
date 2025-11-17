import json
#from src.fileDispositivo import Dispositivo
from src.fileAbastract import AbstractComunicador

class ComunicadorSensores(AbstractComunicador):
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.nombre_archivo = "data/DatosSensores.json"

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
        texto = msg.payload.decode("utf-8")

        if self.gui_callback:
            self.gui_callback(f"[SENSOR][{msg.topic}] {texto}")
"""
        try:
            # Decodificar y convertir el mensaje de JSON a diccionario
            payload = json.loads(msg.payload.decode("utf-8"))
            Dispositivo.guardarDatos(payload, self.nombre_archivo)

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
"""