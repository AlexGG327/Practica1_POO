import tkinter as tk
from tkinter import ttk, Label
from meshtastic import BROADCAST_NUM

from meshtastic_package.mensajes import MensajesFrame
from meshtastic_package.mapa import MapaFrame
from meshtastic_package.robot import RobotFrame
from meshtastic_package.fileComunicador import Comunicador

from rclpy.node import Node

class MainApp(Node):
    def __init__(self):
        super().__init__('meshtastic_node')

        # ------------ MESHTASTIC / MQTT ------------
        self.ordenador = Comunicador()

        self.ordenador.client.on_connect = self.ordenador.on_connect
        self.ordenador.client.on_disconnect = self.ordenador.on_disconnect
        self.ordenador.client.on_message = self.ordenador.on_message

        self.ordenador.callback_mensaje_recibido = self.mostrar_mensaje_recibido

        self.ordenador.connect_mqtt()
        self.get_logger().info("Escuchando mensajes Meshtastic/MQTT...")

        # ------------ TKINTER GUI ------------
        self.root = tk.Tk()
        self.root.title("Meshtastic")
        self.root.geometry("800x650")

        Label(self.root, text="Hola ROS2 + Tkinter").grid(
            row=0, column=0, columnspan=4, pady=10
        )

        # Crear frames
        self.frame_mensajes = MensajesFrame(
            self.root, enviar_callback=self.enviar_mensaje
        )
        self.frame_mapa = MapaFrame(self.root)
        self.frame_robot = RobotFrame(self.root)

        # Botones para cambiar de frame
        top_frame = ttk.Frame(self.root)
        top_frame.grid(row=0, column=0, pady=10)

        ttk.Button(top_frame, text="Mensajes",
                   command=self.mostrar_mensaje).grid(row=0, column=0, padx=5)
        ttk.Button(top_frame, text="Mapa",
                   command=self.mostrar_mapa).grid(row=0, column=1, padx=5)
        ttk.Button(top_frame, text="Robot",
                   command=self.mostrar_robot).grid(row=0, column=2, padx=5)
        ttk.Button(top_frame, text="Salir",
                   command=self.root.destroy).grid(row=0, column=3, padx=5)

        # Mostrar mensajes al iniciar
        self.mostrar_mensaje()

    # ---------- MÉTODOS DE CONTROL DE LA GUI ----------

    def run(self):
        """Lanza el bucle principal de Tkinter."""
        self.root.mainloop()

    # ---------- CALLBACKS ----------

    def mostrar_mensaje_recibido(self, texto: str):
        """Callback que viene de Comunicador (hilo MQTT)."""
        self.root.after(0, lambda: self.frame_mensajes.mostrar_mensaje(texto))

    def mostrar_mensaje(self):
        self.frame_mapa.grid_forget()
        self.frame_robot.grid_forget()
        self.frame_mensajes.grid(row=1, column=0, sticky="nsew")

    def enviar_mensaje(self, texto: str):
        self.ordenador.message_text = texto
        self.get_logger().info(f"Texto a enviar: {self.ordenador.message_text}")
        self.ordenador.send_message(BROADCAST_NUM, False)

    def mostrar_mapa(self):
        self.frame_mensajes.grid_forget()
        self.frame_robot.grid_forget()
        self.frame_mapa.grid(row=1, column=0, sticky="nsew")

    def mostrar_robot(self):
        self.frame_mensajes.grid_forget()
        self.frame_mapa.grid_forget()
        self.frame_robot.grid(row=1, column=0, sticky="nsew")

