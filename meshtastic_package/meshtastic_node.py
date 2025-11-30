#import rclpy
from principal import MainApp
"""
def main(args=None):
    rclpy.init(args=args)
    nodo = MainApp()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
"""
#   ros2 run meshtastic_package mestastic_node

if __name__ == "__main__":
    MainApp()