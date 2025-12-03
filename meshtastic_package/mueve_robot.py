import rclpy
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator

import threading

from typing import TypeVar, Generic

class Mover_Robot:
    def __init__(self):
        #rclpy.init()
        self.navigator = TurtleBot4Navigator()

    def iniciar_turtlebot(self):
        if not self.navigator.getDockedStatus():
            self.navigator.info('Docking')
            self.navigator.dock()

        # Set initial pose
        initial_pose = self.navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
        self.navigator.setInitialPose(initial_pose)

        # Wait for Nav2
        self.navigator.waitUntilNav2Active()

    def undock(self):
        print("Undocking...")
        self.navigator.undock()
        print("Undocked.")

    def dock(self):
        print("Docking...")
        self.navigator.dock()
        print("Docked.")

    def mover_robot_meshtastic(self):
        # Set goal poses
        goal_pose = self.navigator.getPoseStamped([-0.5, 0.0], TurtleBot4Directions.EAST)

        # Undock
        self.navigator.undock()

        # Go to each goal pose
        self.navigator.startToPose(goal_pose)
        

    def mover_robot_meshtastic_posicion(self, x_destino:float, y_destino:float):
        # Set goal poses
        goal_pose = self.navigator.getPoseStamped([x_destino, y_destino], TurtleBot4Directions.EAST)

        # Undock
        self.navigator.undock()

        # Go to each goal pose
        self.navigator.startToPose(goal_pose)

    def apagar_robot(self):
        rclpy.shutdown()

"""
def mueve_turtlebot():
    rclpy.init()

    navigator = TurtleBot4Navigator()
    
    # Start on dock
    if not navigator.getDockedStatus():
        navigator.info('Docking')
        navigator.dock()

    # Set initial pose
    initial_pose = navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
    navigator.setInitialPose(initial_pose)

    # Wait for Nav2
    navigator.waitUntilNav2Active()

    # Set goal poses
    goal_pose = navigator.getPoseStamped([-0.5, 0.0], TurtleBot4Directions.EAST)

    # Undock
    navigator.undock()

    # Go to each goal pose
    navigator.startToPose(goal_pose)

    rclpy.shutdown()
"""