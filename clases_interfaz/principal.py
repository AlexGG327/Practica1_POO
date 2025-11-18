import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import paho.mqtt.client as mqtt
from meshtastic import BROADCAST_NUM

from clases_interfaz.mensajes import MensajesFrame

from src.fileComunicador import Comunicador

class MainApp:
    def __init__(self):
        #NORMAL
        self.ordenador = Comunicador()
        
        self.ordenador.client.on_connect = self.ordenador.on_connect
        self.ordenador.client.on_disconnect = self.ordenador.on_disconnect
        self.ordenador.client.on_message = self.ordenador.on_message

        self.ordenador.callback_mensaje_recibido = self.mostrar_mensaje_recibido

        self.ordenador.connect_mqtt()
        print("Escuchando...")

        #PARA INTERFAZ
        self.root = tk.Tk()
        self.root.title("MQTT / Mensajes")
        self.root.geometry("650x500")

        # Frames
        self.frame_mensajes = MensajesFrame(self.root, enviar_callback=self.enviar_mensaje)

        # Menú/botones para cambiar de vista
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="Mensajes", command=self.mostrar_mensaje).grid(row=0, column=0, padx=5)

        ttk.Button(top_frame, text="Salir", command=self.root.destroy).grid(row=0, column=2, padx=5)

        # Mostrar vista inicial
        self.mostrar_mensaje()

    #CAMBIO DE FRAME

    def mostrar_mensaje_recibido(self, texto):
        self.root.after(0, lambda: self.frame_mensajes.mostrar_mensaje(texto))

    def mostrar_mensaje(self):
        self.frame_mensajes.pack(fill="both", expand=True)

    def enviar_mensaje(self, texto):
        self.ordenador.message_text = self.frame_mensajes.entry.get()
        print("El texto ingresado es:", self.ordenador.message_text)
        self.ordenador.send_message(BROADCAST_NUM, False)
        #canvas.insert(tk.END, "Hola mundo\n")
        
        #Aquí conectas TU lógica real:
        #ordenador.message_text = texto
        #ordenador.send_message(...)
        
        print("Mensaje enviado:", texto)
        self.frame_mensajes.mostrar_mensaje("[TÚ] " + texto)
    
    def run(self):
        self.root.mainloop()