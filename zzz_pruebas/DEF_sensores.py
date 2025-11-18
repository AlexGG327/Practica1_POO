import paho.mqtt.client as mqtt
import json

class ComunicadorSensores():
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback

        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

        self.topics = config["TOPICSsensores"]
        self.broker = config["BROKERsensores"]
        self.port = config["mqtt_port"]

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def iniciar_sensores(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        
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