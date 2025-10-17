from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from meshtastic import BROADCAST_NUM, protocols
import paho.mqtt.client as mqtt
import random
import time
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import re
import json

from fileComunicador import Comunicador
from fileComunicadorSensores import ComunicadorSensores
from fileRefresh import clearConsole

with open("static/config.json", "r", encoding="utf-8") as archivo:
    config = json.load(archivo)

class InterfazTerminal:
    def main(self):

        ordenador = Comunicador()
        
        ordenadorSensores = ComunicadorSensores(self.BROKERsensores, self.mqtt_port, self.TOPICSsensores)

        ordenador.client.on_connect = ordenador.on_connect
        ordenador.client.on_disconnect = ordenador.on_disconnect
        ordenador.client.on_message = ordenador.on_message

        client = mqtt.Client()
        client.on_connect = ordenadorSensores.on_connect
        client.on_message = ordenadorSensores.on_message

        ordenador.connect_mqtt()
        print("Escuchando...")
        
        time.sleep(1)
        
        try:
            ordenador.send_node_info(BROADCAST_NUM, want_response=False)
            time.sleep(4)
            ordenador.send_message(BROADCAST_NUM)
            while True:
                #clearConsole()
                print("Menu:")
                print("1. Enviar mensaje.")
                print("2. Enviar posición.")
                print("3. Enviar info de nodos.")
                print("4. Escuchar sensores.")
                print("5. Clear console.")
                print("6. Desconectar.")
                opcion = input("Selccione una opción: ")
                if opcion == "1":
                    mensaje = input("Escriba el mensaje a enviar: ")
                    ordenador.message_text = mensaje
                    ordenador.send_message(BROADCAST_NUM)
                elif opcion == "2":
                    lat = input("Latitud (0 para no cambiarlo): ")
                    lon = input("Longitud (0 para no cambiarlo): ")
                    alt = input("Altitud (0 para no cambiarlo): ")
                    if lat != "0":
                        ordenador.lat = lat
                    if lon != "0":
                        ordenador.lon = lon
                    if alt != "0":
                        ordenador.alt = alt
                    ordenador.send_position(BROADCAST_NUM)
                elif opcion == "3":
                    ordenador.send_node_info(BROADCAST_NUM, want_response=False)
                elif opcion == "4":
                    client.connect(self.BROKERsensores, self.mqtt_port, 60)
                    print("Esperando mensajes... Presiona Ctrl+C para salir")
                    try:
                        client.loop_forever()  # Mantener el cliente en ejecución
                    except KeyboardInterrupt:
                        print("Desconectando del broker...")
                        client.disconnect()
                elif opcion == "5":
                    clearConsole()
                    print("Consola limpiada.")
                elif opcion == "6":
                    print("Desconectando...")
                    ordenador.disconnect_mqtt()
                    break
                else:
                    print("Opción no válida.")
        except KeyboardInterrupt:
            print("Desconectando...")
            ordenador.disconnect_mqtt()