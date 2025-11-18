import cv2
import numpy as np
import base64
import paho.mqtt.client as mqtt
import keyboard
import time
import mouse

class doom_exe:
    def __init__(self):
        self.topic_transmitir = "transmitir_doom"
        self.topic_imputs = "imputs_doom"
        self.broker = "broker.emqx.io"
        self.port = 1883

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        

    # mensajes doom
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
            # Suscribirse a los temas
            self.client.subscribe(self.topic_transmitir)
            self.client.subscribe(self.topic_imputs)
            print(f"Suscrito al tema '{self.topic_transmitir}'")
        else:
            print(f"Error de conexión, código: {rc}")
            
    # recibir mensajes
    def on_message(self, client, userdata, msg):

        if msg.topic == 'transmitir_doom':
            print(f"Frame recibido en '{self.topic_transmitir}'")
            try:
                # Decodificar base64 a bytes
                frame_bytes = base64.b64decode(msg.payload.decode("utf-8"))
                
                # Convertir bytes a array NumPy
                array = np.frombuffer(frame_bytes, np.uint8)
                
                # Decodificar JPEG a imagen OpenCV
                img = cv2.imdecode(array, cv2.IMREAD_COLOR)
                
                
                # Mostrar la imagen
                cv2.imshow('DOOM - Ventana Completa', img)
                cv2.waitKey(1)  # importante para refrescar ventana
            except Exception as e:
                print("Error decodificando frame:", e)
    
    
    def detectar_imputs(self):
            tecla = 0
            while True:
                tecla = input("Presiona una tecla (w/a/s/d/e/space) para enviar input a DOOM.").lower()
                if tecla == "w":
                    imput = "W"
                    print("Movimiento adelante")
                if tecla == "s":
                    imput = "S"
                    print("Movimiento atrás")
                if tecla == "a":
                    imput = "A"
                if tecla == "d":
                    imput = "D"
                if tecla == "e":
                    imput = "SPACE"
                if tecla =='space':
                    imput = "FIRE"

                if imput is not None:
                    self.client.publish(self.topic_imputs, imput)
                    print(f"Input enviado: {imput}", flush=True)    
                
                time.sleep(0.05)