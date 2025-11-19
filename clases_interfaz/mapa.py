import tkinter as tk
import tkintermapview

from tkinter import ttk, scrolledtext

class MapaFrame(ttk.Frame):
    def __init__(self, parent):
        """
        enviar_callback: función que MainApp llama para enviar mensajes al Comunicador.
        """
        super().__init__(parent, padding=20)

        # --- Título ---
        ttk.Label(self, text="Mapa", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # --- Log de mensajes ---
        self.log = scrolledtext.ScrolledText(self, width=60, height=15, state="disabled")
        self.log.pack(pady=10)

        # --- Entrada + botón ---
        entry_frame = ttk.Frame(self)
        entry_frame.pack(pady=10)

        self.entry = ttk.Entry(entry_frame, width=40)
        self.entry.grid(row=0, column=0, padx=5)

        ttk.Button(text="Leer Posiciones", command=self.leer_posiciones).grid(row=0, column=1)

    def leer_posiciones(self):
        """Envía el mensaje a la función callback (MainApp)."""
        with open("posiciones.txt", "r") as file_posiciones:
            for linea in file_posiciones:
                lista_posicion = linea.split()
                lat = lista_posicion[1] / 10000000
                lon = lista_posicion[3] / 10000000
                texto = f"Latitud: {lat}, Longitud: {lon}"
                print(texto)

                map_widget.set_marker(float(lat), float(lon))