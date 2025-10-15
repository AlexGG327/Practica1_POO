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

debug = True

class Dispositivo:
    def __init__(self, lat, lon, alt, root_topic, channel):
        self.tls_configured = False

        self.root_topic = root_topic
        self.channel = channel

        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.random_hex_chars = "a8a1"
        self.node_name = '!abcd' + self.random_hex_chars
        self.node_number = int(self.node_name.replace("!", ""), 16)
        self.set_topic()

    def set_topic(self): #Dispositivo
        # Prepara variables para MQTT
        if debug: print("set_topic")
        self.node_name = '!' + hex(self.node_number)[2:] # Identificador del nodo, en hexadecimal  para MQTT
        self.subscribe_topic = self.root_topic + self.channel + "/#" # Donde escuchar
        self.publish_topic = self.root_topic + self.channel + "/" + self.node_name # Donde publicar


"""
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If computer is running windows use cls
        command = 'cls'
    os.system(command)

clearConsole()
"""