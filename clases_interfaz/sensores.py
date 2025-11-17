import tkinter as tk
from tkinter import ttk, scrolledtext

# ===========================================================
#   FRAME PARA SENSORES
# ===========================================================

class SensoresFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        ttk.Label(self, text="Sensores", font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.log = scrolledtext.ScrolledText(self, width=60, height=15, state="disabled")
        self.log.pack(pady=10)

        ttk.Button(self, text="Inciar escucha").pack(pady=10)

    def mostrar_mensaje(self, texto):
        self.log.config(state="normal")
        self.log.insert("end", texto + "\n")
        self.log.see("end")
        self.log.config(state="disabled")
        
        ttk.Label(self, text="Aquí se mostrarán los datos de sensores.").pack(pady=20)