import threading
import rclpy
from rclpy.executors import MultiThreadedExecutor
from meshtastic_package.principal import MainApp


def ros_spin(app):
    # Ya NO llamamos a rclpy.init aquí
    executor = MultiThreadedExecutor()
    executor.add_node(app)

    app.executor = executor

    print("ROS2 executor running in background thread")
    executor.spin()

    app.destroy_node()


def main(args=None):
    # 1) Inicializar ROS ANTES de crear MainApp
    rclpy.init(args=args)

    # 2) Crear MainApp (ya no dará error)
    app = MainApp()

    # 3) Lanzar ROS en segundo plano
    ros_thread = threading.Thread(target=ros_spin, args=(app,), daemon=True)
    ros_thread.start()

    # 4) Tkinter en el hilo principal
    app.run()

    # 5) Al salir de la GUI → apagar ROS
    rclpy.shutdown()


if __name__ == "__main__":
    main()
