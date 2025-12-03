#   ros2 run meshtastic_package mestastic_node

import threading

import rclpy
from meshtastic_package.principal import MainApp

def main(args=None):
    # Inicializa ROS 2
    rclpy.init(args=args)

    # Crea el nodo (que también monta la GUI Tkinter)
    nodo = MainApp()

    # Lanza el spin de ROS2 en un hilo en segundo plano
    spin_thread = threading.Thread(target=rclpy.spin, args=(nodo,), daemon=True)
    spin_thread.start()

    try:
        # Bucle principal de Tkinter en el hilo principal
        nodo.run()
    finally:
        # Al cerrar la ventana, paramos ROS2
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()