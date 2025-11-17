import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from src.fileComunicador import Comunicador

import threading

from meshtastic import BROADCAST_NUM
import paho.mqtt.client as mqtt
import json
import time

ordenador = Comunicador()

with open("static/config.json", "r", encoding="utf-8") as archivo:
    config = json.load(archivo)
BROKERsensores = config["BROKERsensores"]
mqtt_port = config["mqtt_port"]

ordenador.client.on_connect = ordenador.on_connect
ordenador.client.on_disconnect = ordenador.on_disconnect
ordenador.client.on_message = ordenador.on_message

client = mqtt.Client()

ordenador.connect_mqtt()
print("Escuchando...")

time.sleep(1)

root = tk.Tk()
root.title("Mensajes MQTT")

frm = ttk.Frame(root, padding=500)
frm.grid()
ttk.Button(frm, text="Cerrar", command=root.destroy).grid(column=20, row=20)
ttk.Button(frm, text="Interfaz Mensaje").grid(column=1, row=1)
ttk.Button(frm, text="Escuchar Sensores").grid(column=2, row=1)
texto = "Mensaje desde interfaz grafica"

main_frame = ttk.Frame(frm,padding=250)

canvas = scrolledtext.ScrolledText(root, wrap=tk.WORD ,width=40, height=10, state="disabled", font=("courier", 10))
canvas.config(state="normal")
canvas.grid(padx=10, pady=10)
canvas.insert(tk.END, "Hola mundo\n")
canvas.see(tk.END)

entrada_texto = ttk.Entry(root)

# Posicionar el widget en la ventana
entrada_texto.grid(padx=10, pady=10)

# Función para obtener el texto
def enviar_mensajes_grafica():
    ordenador.message_text = entrada_texto.get()
    print("El texto ingresado es:", ordenador.message_text)
    ordenador.send_message(BROADCAST_NUM, False)
    canvas.insert(tk.END, "Hola mundo\n")

def actualizar_canvas():
    mensaje = ordenador.lista_mensajes_grafica(-1)
    
boton = ttk.Button(text="Enviar Mensaje", command=enviar_mensajes_grafica)
boton.grid(pady=5)


root.mainloop()
