import threading
from tkinter import ttk
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator

class RobotFrame():
    def __init__(self):
        self.navigator = None

        self.posicion_x = 0.0
        self.posicion_y = 0.0

    def run(self, fn, x, y):
        self.posicion_x = x
        self.posicion_y = y
        if fn == "undock":
            threading.Thread(target=self.undock, daemon=True).start()

        elif fn == "dock":
            threading.Thread(target=self.dock, daemon=True).start()

        elif fn == "iniciar":
            threading.Thread(target=self.iniciar, daemon=True).start()

        elif fn == "mover":
            threading.Thread(target=self.mover, daemon=True).start()

        elif fn == "mover_posicion":
            print(f"Posición objetivo establecida en x: {self.posicion_x}, y: {self.posicion_y}")
            threading.Thread(target=self.mover_a_posicion, daemon=True).start()

    # Iniciar navigator
    def get_nav(self):
        if self.navigator is None:
            print("Inicializando TurtleBot4Navigator...")
            self.navigator = TurtleBot4Navigator()
        return self.navigator

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

        print("Moviéndose al objetivo...")
        nav.startToPose(goal)

    def mover_a_posicion(self):
        nav = self.get_nav()

        goal = nav.getPoseStamped([self.posicion_x, self.posicion_y], TurtleBot4Directions.EAST)

        nav.undock()

        print("Moviéndose al objetivo...")
        nav.startToPose(goal)