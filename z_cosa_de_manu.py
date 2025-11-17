import cv2
import numpy as np
import base64
import paho.mqtt.client as mqtt

class doom_exe:
    
    def __init__(self):
        self.topic_doom = "transmitir_doom"
        self.broker = "broker.emqx.io"
        self.port = 1883

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, 1883, 60)
        self.client.loop_start()
        
        
    # mensajes doom
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            client.subscribe(self.topic_doom)
            print(f"Suscrito al tema '{self.topic_doom}'")
        else:
            print(f"Error de conexión, código: {rc}")
            
    # recibir mensajes
    def on_message(self, client, userdata, msg):
        if msg.topic == self.topic_doom:
            print(f"Frame recibido en '{self.topic_doom}'")
            try:
                # Decodificar base64 a bytes
                frame_bytes = base64.b64decode(msg.payload.decode("utf-8"))
                
                # Convertir bytes a array NumPy
                nparr = np.frombuffer(frame_bytes, np.uint8)
                
                # Decodificar JPEG a imagen OpenCV
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Mostrar la imagen
                cv2.imshow('DOOM - Ventana Completa', img)
                cv2.waitKey(1)  # importante para refrescar ventana
            except Exception as e:
                print("Error decodificando frame:", e)

if __name__ == "__main__":
    app = doom_exe()
    app.on_connect()