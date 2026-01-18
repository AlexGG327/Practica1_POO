import tkinter as tk
import tkintermapview
import json

from tkinter import ttk, scrolledtext

class MapaFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        
        #Titulo
        ttk.Label(self, text="Mapa", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.map_widget = tkintermapview.TkinterMapView(self, width=600, height=400)
        self.map_widget.grid(row=1, column=0, columnspan=2, pady=10)

        self.map_widget.set_position(42.6863, -2.9476)
        self.map_widget.set_zoom(15)

        ttk.Button(entry_frame, text="Actualizar mapa", command=self.leer_posiciones).grid(row=1, column=1)

    def leer_posiciones(self):
        patth = "/home/alexg/turtlebot4_ws/install/meshtastic_package/share/meshtastic_package/data/"

        with open(patth + "mensaje_posicion_recibido.json", "r") as file_posiciones:
            datos_posiciones = json.load(file_posiciones)

        for linea in datos_posiciones:
            lista_posicion = linea.split()
            lat = int(lista_posicion[1]) / 10000000
            lon = int(lista_posicion[3]) / 10000000
            #texto = f"Latitud: {lat}, Longitud: {lon}"

            self.map_widget.set_marker(float(lat), float(lon))