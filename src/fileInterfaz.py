from meshtastic import BROADCAST_NUM
import paho.mqtt.client as mqtt
import time
import json

from src.fileComunicador import Comunicador
from src.fileComunicadorSensores import ComunicadorSensores
from src.fileDispositivo import Dispositivo


class InterfazTerminal:
    def __init__(self):
        self.ordenador = Comunicador()

        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
        self.BROKERsensores = config["BROKERsensores"]
        self.mqtt_port = config["mqtt_port"]
        ordenadorSensores = ComunicadorSensores()

        self.ordenador.client.on_connect = self.ordenador.on_connect
        self.ordenador.client.on_disconnect = self.ordenador.on_disconnect
        self.ordenador.client.on_message = self.ordenador.on_message

        self.client = mqtt.Client()
        self.client.on_connect = ordenadorSensores.on_connect
        self.client.on_message = ordenadorSensores.on_message

        self.ordenador.connect_mqtt()
        print("Escuchando...")
        
        time.sleep(1)

    def main(self):

        self.ordenador.send_node_info(BROADCAST_NUM, want_response=False)
        time.sleep(4)
        #self.ordenador.send_message(BROADCAST_NUM, False)
        time.sleep(2)

        while True:
            print("\n")
            print("Menu:")
            print("1. Enviar mensaje.")
            print("2. Enviar mensaje directo")
            print("3. Enviar posición.")
            print("4. Enviar info de nodos.")
            print("5. Escuchar sensores.")
            print("6. Clear console.")
            print("7. Desconectar.")
            opcion = input("Selccione una opción: ")

            if opcion == "1":
                mensaje = input("Escriba el mensaje a enviar: ")
                self.ordenador.message_text = mensaje
                self.ordenador.send_message(BROADCAST_NUM, False)

            elif opcion == "2":
                mensaje = input("Escriba el mensaje a enviar: ")
                self.ordenador.message_text = mensaje
                self.ordenador.send_message(BROADCAST_NUM, True)

            elif opcion == "3":
                lat = input("Latitud (0 para no cambiarlo): ")
                lon = input("Longitud (0 para no cambiarlo): ")
                alt = input("Altitud (0 para no cambiarlo): ")
                if lat != "0":
                    self.ordenador.lat = lat
                if lon != "0":
                    self.ordenador.lon = lon
                if alt != "0":
                    self.ordenador.alt = alt
                self.ordenador.send_position(BROADCAST_NUM)

            elif opcion == "4":
                self.ordenador.send_node_info(BROADCAST_NUM, want_response=False)

            elif opcion == "5":
                self.client.connect(self.BROKERsensores, self.mqtt_port, 60)
                print("Esperando mensajes... Presiona Ctrl+C para salir")
                try:
                    self.client.loop_forever()  # Mantener el cliente en ejecución
                except KeyboardInterrupt:
                    print("Desconectando del broker...")
                    self.client.disconnect()

            elif opcion == "6":
                Dispositivo.clearConsole()
                print("Consola limpiada.")

            elif opcion == "7":
                Dispositivo.clearConsole()
                print("Desconectando...")
                self.ordenador.disconnect_mqtt()
                break
            else:
                Dispositivo.clearConsole()
                print("Opción no válida.")