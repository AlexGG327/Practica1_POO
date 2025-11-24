import cv2
import numpy as np
import base64
import paho.mqtt.client as mqtt
import time
import pygame

class doom_exe:
    
    def __init__(self):
        self.topic_transmitir = "transmitir_doom"
        self.topic_imputs = "imputs_doom"
        self.broker = "broker.emqx.io"
        self.port = 1883

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, 1883, 60)
        self.ultimo_frame = None
        
        # Inicializar pygame
        pygame.init()
        self.ventana = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("DOOM - Receptor")
        
        
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

                # Convertir de BGR (OpenCV) a RGB (Pygame)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Guardar el frame
                self.ultimo_frame = img_rgb
                
                # Mostrar la imagen
                #cv2.imshow('DOOM - Ventana Completa', img)
                #cv2.waitKey(1) 
            except Exception as e:
                print("Error decodificando frame:", e)
    
    
    def detectar_imputs(self):
        imput = None
        while True:
            # Procesar eventos
            for event in pygame.event.get():
                # Actualizar la pantalla SIEMPRE, no solo cuando hay eventos
                if self.ultimo_frame is not None:
                    surf = pygame.surfarray.make_surface(np.transpose(self.ultimo_frame, (1, 0, 2)))
                    self.ventana.blit(surf, (0, 0))
                else:
                    self.ventana.fill((0, 0, 0))
                
                pygame.display.flip()
            
                tecla = pygame.key.get_pressed()
                if tecla[pygame.K_w]:
                    imput = 'w'
                    print("W presionada")
                if tecla[pygame.K_a]:
                    imput = 'a'
                    print("A presionada")
                if tecla[pygame.K_s]:
                    imput = 's'
                    print("S presionada")
                if tecla[pygame.K_d]:
                    imput = 'd'
                    print("D presionada")
                if tecla[pygame.K_SPACE]:
                    imput = 'espacio' 
                    print("espacio presionada")
                if pygame.mouse.get_pressed()[0]:
                    imput = 'click_izquierdo'
                    print("click izquierdo presionado")


                if imput is not None:
                    self.client.publish(self.topic_imputs, imput)
                    print("Imput enviado:", imput)
                time.sleep(0.05)

def main():
    doom = doom_exe()
    doom.client.loop_start()
    doom.detectar_imputs()

if __name__ == "__main__":
    main()