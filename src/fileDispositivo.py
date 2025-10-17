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

debug = True

class Dispositivo:
    def __init__(self, root_topic, channel):
        self.tls_configured = False

        self.root_topic = root_topic
        self.channel = channel

        self.random_hex_chars = "a8a1"
        self.node_name = '!abcd' + self.random_hex_chars
        self.node_number = int(self.node_name.replace("!", ""), 16)
        self.set_topic()

    def set_topic(self):
        # Prepara variables para MQTT
        if debug: print("set_topic")
        self.node_name = '!' + hex(self.node_number)[2:] # Identificador del nodo, en hexadecimal  para MQTT
        self.subscribe_topic = self.root_topic + self.channel + "/#" # Donde escuchar
        self.publish_topic = self.root_topic + self.channel + "/" + self.node_name # Donde publicar
    
    @staticmethod
    def guardarDatos(nuevo_datos, nombreArchivo):

        with open(nombreArchivo, "r", encoding = "utf-8") as archivo:
            try:
                datosExistentes = json.load(archivo)
                if not isinstance(datosExistentes, list):
                    datosExistentes = [datosExistentes]
            except json.JSONDecodeError:
                datosExistentes = []
        datosExistentes.append(nuevo_datos)

        with open(nombreArchivo, "w", encoding = "utf-8") as archivo:
            json.dump(datosExistentes, archivo, indent = 4, ensure_ascii = False)

    @staticmethod
    def guardarContactos(contacto, nombreArchivo):
        try:
            with open(nombreArchivo, "r", encoding = "utf-8") as archivo:
                datosExistentes = json.load(archivo)
                if not isinstance(datosExistentes, list):
                    datosExistentes = [datosExistentes]
        except json.JSONDecodeError:
            datosExistentes = []

        # Verificar si el contacto ya existe
        for existente in datosExistentes:
            if contacto == existente["codigo"]:
                #print("El contacto ya existe:", existente)
                return
            
        nuevo_contacto = {"codigo": contacto, "nombre": ""}
        datosExistentes.append(nuevo_contacto)
        print("Nuevo contacto conseguido")

        with open(nombreArchivo, "w", encoding = "utf-8") as archivo:
            json.dump(datosExistentes, archivo, indent = 4, ensure_ascii = False)