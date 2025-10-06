# Powered by Meshtastic™ https://meshtastic.org/

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
from fileInterfaz import InterfazTerminal

#### Debug Options
debug = True
auto_reconnect = True
auto_reconnect_delay = 1 # seconds
print_service_envelope = False
print_message_packet = False

print_node_info =  True
print_node_position = True
print_node_telemetry = True

# Program Base Functions

if __name__ == "__main__":


    programa = InterfazTerminal()

    programa.main()