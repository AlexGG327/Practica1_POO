import threading
from tkinter import ttk
from turtlebot4_navigation.turtlebot4_navigator import (
    TurtleBot4Directions,
    TurtleBot4Navigator
)


class RobotFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        # IMPORTANTE:
        # El navigator debe crearse DESPUÉS de que ROS ya está inicializado.
        # por eso lo creamos con lazy-init
        self.navigator = None

        ttk.Label(self, text="Robot", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Button(self, text="Undock", command=lambda: self.run(self.undock)).grid(row=1, column=0)
        ttk.Button(self, text="Dock",   command=lambda: self.run(self.dock)).grid(row=1, column=1)
        ttk.Button(self, text="Iniciar Turtlebot4", command=lambda: self.run(self.iniciar)).grid(row=1, column=2)
        ttk.Button(self, text="Moverse", command=lambda: self.run(self.mover)).grid(row=1, column=3)

    def run(self, fn):
        threading.Thread(target=fn, daemon=True).start()

    # ------------------------------------------
    # Lazy init del Navigator
    # ------------------------------------------
    def get_nav(self):
        if self.navigator is None:
            print("Inicializando TurtleBot4Navigator...")
            self.navigator = TurtleBot4Navigator()
        return self.navigator

    # ------------------------------------------
    # ACCIONES DEL ROBOT
    # ------------------------------------------
    def undock(self):
        nav = self.get_nav()
        print("Undocking...")
        nav.undock()
        print("Undocked.")

    def dock(self):
        nav = self.get_nav()
        print("Docking...")
        nav.dock()
        print("Docked.")

    def iniciar(self):
        nav = self.get_nav()
        print("Iniciando TurtleBot4...")

        if not nav.getDockedStatus():
            nav.dock()

        pose = nav.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
        nav.setInitialPose(pose)

        nav.waitUntilNav2Active()

        print("Turtlebot4 iniciado.")

    def mover(self):
        nav = self.get_nav()

        goal = nav.getPoseStamped([-13.0, 9.0], TurtleBot4Directions.EAST)

        nav.undock()
        nav.startToPose(goal)

        print("Moviéndose al objetivo...")
