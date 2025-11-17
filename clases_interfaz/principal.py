import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import paho.mqtt.client as mqtt
from meshtastic import BROADCAST_NUM


from clases_interfaz.mensajes import MensajesFrame
from clases_interfaz.sensores import SensoresFrame

from src.fileComunicador import Comunicador
from clases_interfaz.DEF_sensores import ComunicadorSensores

# ===========================================================
#   APP PRINCIPAL
# ===========================================================

class MainApp:
    def __init__(self):
        #NORMAL
        self.ordenador = Comunicador()

        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

        self.BROKERsensores = config["BROKERsensores"]
        self.mqtt_port = config["mqtt_port"]
        ordenadorSensores = ComunicadorSensores()

        self.ordenador.client.on_connect = self.ordenador.on_connect
        self.ordenador.client.on_disconnect = self.ordenador.on_disconnect
        self.ordenador.client.on_message = self.ordenador.on_message

        self.client = mqtt.Client()
        self.client.on_connect = ordenadorSensores.on_connect
        self.client.on_message = ordenadorSensores.on_message

        self.ordenador.connect_mqtt()
        print("Escuchando...")

        #PARA INTERFAZ
        self.root = tk.Tk()
        self.root.title("MQTT / Mensajes / Sensores")
        self.root.geometry("650x500")

        self.sensores = ComunicadorSensores(gui_callback=self.recibir_sensor)

        # Frames
        self.frame_mensajes = MensajesFrame(self.root, enviar_callback=self.enviar_mensaje)
        self.frame_sensores = SensoresFrame(self.root)

        # Menú/botones para cambiar de vista
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="Mensajes", command=self.mostrar_mensajes).grid(row=0, column=0, padx=5)
        ttk.Button(top_frame, text="Sensores", command=self.mostrar_sensores).grid(row=0, column=1, padx=5)

        ttk.Button(top_frame, text="Salir", command=self.root.destroy).grid(row=0, column=2, padx=5)

        # Mostrar vista inicial
        self.mostrar_mensajes()

    # =======================================================
    #   CALLBACKS Y LÓGICA DE CAMBIO DE FRAME
    # =======================================================

    def mostrar_mensajes(self):
        self.frame_sensores.pack_forget()
        self.frame_mensajes.pack(fill="both", expand=True)

    def mostrar_sensores(self):
        self.frame_mensajes.pack_forget()
        self.frame_sensores.pack(fill="both", expand=True)

    def enviar_mensaje(self, texto):
        self.ordenador.message_text = self.frame_mensajes.entry.get()
        print("El texto ingresado es:", self.ordenador.message_text)
        self.ordenador.send_message(BROADCAST_NUM, False)
        #canvas.insert(tk.END, "Hola mundo\n")
        """
        Aquí conectas TU lógica real:
        ordenador.message_text = texto
        ordenador.send_message(...)
        """
        print("Mensaje enviado:", texto)
        self.frame_mensajes.mostrar_mensaje("[TÚ] " + texto)

    def recibir_sensor(self, texto):
        self.root.after(0, lambda: self.frame_sensores.mostrar_mensaje(texto))

        self.client.on_connect(self.BROKERsensores, self.mqtt_port, 60)
        self.client.loop_forever()
        # Asegura que se ejecute en el hilo Tkinter
        
    def run(self):
        self.root.mainloop()