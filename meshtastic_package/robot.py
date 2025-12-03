import tkinter as tk
import json
from tkinter import ttk, scrolledtext
import threading

import rclpy
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from meshtastic_package.mueve_robot import Mover_Robot

class RobotFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Robot", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        """
        self.clase_robot = Mover_Robot()

        threading.Thread(target=self.clase_robot.iniciar_turtlebot).start()

        self.hilo_undock = threading.Thread(target=self.clase_robot.undock, daemon=True)
        self.hilo_dock = threading.Thread(target=self.clase_robot.dock, daemon=True)
        
        ttk.Button(entry_frame, text="Undock", command=self.clase_robot.undock).grid(row=1, column=1)
        ttk.Button(entry_frame, text="Dock", command=self.clase_robot.dock).grid(row=1, column=2)
        #ttk.Button(entry_frame, text="Iniciar Turtlebot4", command=self.iniciar_turtlebot).grid(row=1, column=3)
        ttk.Button(entry_frame, text="Moverse", command=self.clase_robot.mover_robot_meshtastic).grid(row=1, column=3)"""

    def threaded_undock(self):
        self.hilo_undock.start()
        self.hilo_undock.join()

    def threaded_dock(self):
        self.hilo_dock.start()
        self.hilo_dock.join()

    def mover_robot_meshtastic(self):
        self.clase_robot.mover_robot_meshtastic()

    def mover_robot_meshtastic_posicion(self,poscionx:float,posciony:float):
        self.clase_robot.mover_robot_meshtastic_posicion(poscionx, posciony)
    def dock(self):
        self.clase_robot.dock_rob()
    def undock(self):
        self.clase_robot.undock_rob()