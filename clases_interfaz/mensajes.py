import tkinter as tk
from tkinter import ttk, scrolledtext

class MensajesFrame(ttk.Frame):
    def __init__(self, parent, enviar_callback):
        super().__init__(parent, padding=20)
        
        #enviar_callback: función que MainApp llama para enviar mensajes al Comunicador.
        self.enviar_callback = enviar_callback

        # --- Título ---
        ttk.Label(self, text="Mensajes", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        #Mensajes recibidos
        self.log = scrolledtext.ScrolledText(self, width=60, height=15, state="disabled")
        self.log.grid(row=1, column=0, columnspan=2, pady=10)

        #Entrada y boton
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.entry = ttk.Entry(entry_frame, width=40)
        self.entry.grid(row=0, column=0, padx=5)

        ttk.Button(entry_frame, text="Enviar", command=self.enviar_desde_gui).grid(row=0, column=1)

    def enviar_desde_gui(self):
        """Envía el mensaje a la función callback (MainApp)."""
        texto = self.entry.get().strip()
        if texto:
            self.enviar_callback(texto)
            self.entry.delete(0, "end")

    def mostrar_mensaje(self, texto):
        """Añade texto al log."""
        self.log.config(state="normal")
        self.log.insert("end", texto + "\n")
        self.log.see("end")
        self.log.config(state="disabled")