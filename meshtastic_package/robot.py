import tkinter as tk
import json
from tkinter import ttk, scrolledtext
import threading

import rclpy
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator

class RobotFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        #rclpy.init()
        self.navigator = TurtleBot4Navigator()

        #Titulo
        ttk.Label(self, text="Robot", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(entry_frame, text="Undock", command=self.undock).grid(row=1, column=1)
        ttk.Button(entry_frame, text="Dock", command=self.dock).grid(row=1, column=2)
        ttk.Button(entry_frame, text="Iniciar Turtlebot4", command=self.iniciar_turtlebot).grid(row=1, column=3)

    def threaded_undock(self):
        threading.Thread(target=self.undock).start()

    def threaded_dock(self):
        threading.Thread(target=self.dock).start()

    def threaded_iniciar_turtlebot(self):
        threading.Thread(target=self.iniciar_turtlebot).start()

    def undock(self):
        print("Undocking...")
        self.navigator.undock()
        print("Undocked.")

    def dock(self):
        print("Docking...")
        self.navigator.dock()
        print("Docked.")

    def iniciar_turtlebot(self):        
        print("Iniciando Turtlebot4...")

        # Start on dock
        if not self.navigator.getDockedStatus():
            self.navigator.info('Docking')
            self.navigator.dock()
        
        # Set initial pose
        initial_pose = self.navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
        self.navigator.setInitialPose(initial_pose)

        print("Turtlebot4 iniciado.")

        """
        # Wait for Nav2
        navigator.waitUntilNav2Active()

        # Set goal poses
        goal_pose = navigator.getPoseStamped([-13.0, 9.0], TurtleBot4Directions.EAST)

        # Undock
        navigator.undock()

        # Go to each goal pose
        navigator.startToPose(goal_pose)

        rclpy.shutdown()
        """