from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from meshtastic import protocols
import paho.mqtt.client as mqtt
import random
import time
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import re
import json

from src.fileDispositivo import Dispositivo
from src.fileAbastract import AbstractComunicador, RecibirMensaajesGenerico

def num_to_id(num):
    """Convierte un número de nodo Meshtastic a su representación tipo !abcd1234"""
    return f"!{num:08x}"

class Comunicador(AbstractComunicador, RecibirMensaajesGenerico):
    def __init__(self):
        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
        
        self.debug = config["debug"]
        self.auto_reconnect = config["auto_reconnect"]
        self.auto_reconnect_delay = config["auto_reconnect_delay"]
        self.print_service_envelope = config["print_service_envelope"]
        self.print_message_packet = config["print_message_packet"]

        self.print_node_info =  config["print_node_info"]
        self.print_node_position = config["print_node_position"]
        self.print_node_telemetry = config["print_node_telemetry"]
        
        self.lat = config["lat"]
        self.lon = config["lon"]
        self.alt = config["alt"]

        self.mqtt_port = config["mqtt_port"]
        self.root_topic = config["root_topic"]
        self.channel = config["channel"]
        self.key = config["key"]
        self.mqtt_broker = config["mqtt_broker"]
        self.mqtt_username = config["mqtt_username"]
        self.mqtt_password = config["mqtt_password"]
        self.message_text = config["message_text"]

        self.client_short_name = config["client_short_name"]
        self.client_long_name = config["client_long_name"]
        self.client_hw_model = config["client_hw_model"]

        self.global_message_id = random.getrandbits(32)

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="", clean_session=True, userdata=None)
        self.dispositivo = Dispositivo(self.root_topic, self.channel, self.debug)

    # Conectar al servidor MQTT

    def connect_mqtt(self):
        if "tls_configured" not in self.connect_mqtt.__dict__:          #Persistent variable to remember if we've configured TLS yet
            self.tls_configured = False

        if self.debug: print("connect_mqtt")
        if not self.client.is_connected():
            try:
                if ':' in self.mqtt_broker:
                    self.mqtt_broker,self.mqtt_port = self.mqtt_broker.split(':')
                    self.mqtt_port = int(self.mqtt_port)

                if self.key == "AQ==":
                    if self.debug: print("key is default, expanding to AES128")
                    self.key = "1PG7OiApB1nwvP+rz05pAQ=="

                padded_key = self.key.ljust(len(self.key) + ((4 - (len(self.key) % 4)) % 4), '=')
                replaced_key = padded_key.replace('-', '+').replace('_', '/')
                self.key = replaced_key

                self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
                if self.mqtt_port == 8883 and self.connect_mqtt.tls_configured == False:
                    self.client.tls_set(ca_certs="cacert.pem", tls_version=ssl.PROTOCOL_TLSv1_2)
                    self.client.tls_insecure_set(False)
                    self.tls_configured = True
                self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
                self.client.loop_start()

            except Exception as e:
                print (e)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        self.dispositivo.set_topic()
        if self.client.is_connected():
            print("client is connected")
        
        if reason_code == 0:
            if self.debug: print(f"Connected to sever: {self.mqtt_broker}")
            if self.debug: print(f"Subscribe Topic is: {self.dispositivo.subscribe_topic}")
            if self.debug: print(f"Publish Topic is: {self.dispositivo.publish_topic}\n")
            self.client.subscribe(self.dispositivo.subscribe_topic)

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        if self.debug: print("on_disconnect")
        if reason_code != 0:
            if self.auto_reconnect == True:
                print("attempting to reconnect in " + str(self.auto_reconnect_delay) + " second(s)")
                time.sleep(self.auto_reconnect_delay)
                self.connect_mqtt()

    def disconnect_mqtt(self):
        if self.debug: print("disconnect_mqtt")
        if self.client.is_connected():
            self.client.disconnect()

    # Enviar mensajes

    def send_message(self, destination_id, Directo_o_noDirecto):
        if Directo_o_noDirecto == True:
            with open("data/contactos.json", "r", encoding="utf-8") as archivo:
                contactos = json.load(archivo)
                print("Contacto a elegir (escribe el numero (0-...)):")
                numero = -1
                for contacto in contactos:
                    numero = numero + 1
                    print(f"Numero: {numero} Nombre: {contacto['nombre']}")
                eleccion = int(input("Elige el numero del contacto: "))
                destination_id = contactos[eleccion]["numero"]
        if not self.client.is_connected():
            self.connect_mqtt()

        if self.message_text:
            encoded_message = mesh_pb2.Data()
            encoded_message.portnum = portnums_pb2.TEXT_MESSAGE_APP 
            encoded_message.payload = self.message_text.encode("utf-8")
            self.generate_mesh_packet(destination_id, encoded_message)
        else:
            return

    def send_traceroute(self, destination_id):
        if not self.client.is_connected():
            self.connect_mqtt()
        if self.debug: print(f"Sending Traceroute Packet to {str(destination_id)}")

        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.TRACEROUTE_APP
        encoded_message.want_response = True

        destination_id = int(destination_id[1:], 16)
        self.generate_mesh_packet(destination_id, encoded_message)

    def send_node_info(self, destination_id, want_response):
        if self.client.is_connected():
            user_payload = mesh_pb2.User()
            setattr(user_payload, "id", self.dispositivo.node_name)
            setattr(user_payload, "long_name", self.client_long_name)
            setattr(user_payload, "short_name", self.client_short_name)
            setattr(user_payload, "hw_model", self.client_hw_model)

            user_payload = user_payload.SerializeToString()

            encoded_message = mesh_pb2.Data()
            encoded_message.portnum = portnums_pb2.NODEINFO_APP
            encoded_message.payload = user_payload
            encoded_message.want_response = want_response  # Request NodeInfo back
            self.generate_mesh_packet(destination_id, encoded_message)

    def send_position(self, destination_id):
        if self.client.is_connected():
            pos_time = int(time.time())
            latitude = int(float(self.lat) * 1e7)
            longitude = int(float(self.lon) * 1e7)
            altitude_units = 1 / 3.28084 if 'ft' in str(self.alt) else 1.0
            altitude = int(altitude_units * float(re.sub('[^0-9.]', '', str(self.alt))))

            position_payload = mesh_pb2.Position()
            setattr(position_payload, "latitude_i", latitude)
            setattr(position_payload, "longitude_i", longitude)
            setattr(position_payload, "altitude", altitude)
            setattr(position_payload, "time", pos_time)

            position_payload = position_payload.SerializeToString()

            encoded_message = mesh_pb2.Data()
            encoded_message.portnum = portnums_pb2.POSITION_APP
            encoded_message.payload = position_payload
            encoded_message.want_response = True

            self.generate_mesh_packet(destination_id, encoded_message)

    def send_ack(self, destination_id, message_id):
        if self.debug: print("Sending ACK")
        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.ROUTING_APP
        encoded_message.request_id = message_id
        encoded_message.payload = b"\030\000"
        self.generate_mesh_packet(destination_id, encoded_message)

    """Estas funciones estaban llaman a generate_mesh_packet"""

    def generate_mesh_packet(self, destination_id, encoded_message):
        mesh_packet = mesh_pb2.MeshPacket()

        # Use the global message ID and increment it for the next call
        mesh_packet.id = self.global_message_id
        self.global_message_id += 1
        
        setattr(mesh_packet, "from", self.dispositivo.node_number)
        mesh_packet.to = destination_id
        mesh_packet.want_ack = False
        mesh_packet.channel = self.generate_hash()
        mesh_packet.hop_limit = 3

        if self.key == "":
            mesh_packet.decoded.CopyFrom(encoded_message)
        else:
            mesh_packet.encrypted = self.encrypt_message(mesh_packet, encoded_message)

        service_envelope = mqtt_pb2.ServiceEnvelope()
        service_envelope.packet.CopyFrom(mesh_packet)
        service_envelope.channel_id = self.channel
        service_envelope.gateway_id = self.dispositivo.node_name

        payload = service_envelope.SerializeToString()
        self.client.publish(self.dispositivo.publish_topic, payload)

    """generarate_mesh_packet llama a encrypt_message y generate_hash"""

    def encrypt_message(self, mesh_packet, encoded_message):
        mesh_packet.channel = self.generate_hash()
        key_bytes = base64.b64decode(self.key.encode('ascii'))
        nonce_packet_id = mesh_packet.id.to_bytes(8, "little")
        nonce_from_node = self.dispositivo.node_number.to_bytes(8, "little")
        nonce = nonce_packet_id + nonce_from_node
        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_bytes = encryptor.update(encoded_message.SerializeToString()) + encryptor.finalize()
        return encrypted_bytes

    def generate_hash(self):

        replaced_key = self.key.replace('-', '+').replace('_', '/')
        key_bytes = base64.b64decode(replaced_key.encode('utf-8')) # Convierta la key en bytes
        h_name = self.xor_hash(bytes(self.channel, 'utf-8')) # Encripta los bytes del nombre
        h_key = self.xor_hash(key_bytes) # Encripta los bytes de la key
        result = h_name ^ h_key # Combina ambos hashes
        return result
    
    """generate_hash usa xor_hash"""
    
    def xor_hash(self, data):
        # Como encriptar
        result = 0
        for char in data:
            result ^= char
        return result

    # Recivir mensajes

    def on_message(self, client, userdata, msg):
        # Interpreta los mensajes recibidos de meshtastic a través de MQTT
        se = mqtt_pb2.ServiceEnvelope()
        try: # Se asegura de que el mensaje es correcto
            se.ParseFromString(msg.payload)
            if self.print_service_envelope:
                print ("")
                print ("Service Envelope:")
                print (se)
            mp = se.packet
            if self.print_message_packet: 
                print ("")
                print ("Message Packet:")
                print(mp)
        except Exception as e:
            print(f"*** ServiceEnvelope: {str(e)}")
            return
        
        if mp.HasField("encrypted") and not mp.HasField("decoded"): # Si el mensaje está encriptado y no decodificado
            self.decode_encrypted(mp)
    
        # Attempt to process the decrypted or encrypted payload
        portNumInt = mp.decoded.portnum if mp.HasField("decoded") else None # Obtiene el número de puerto que indica el tipo de mensaje
        handler = protocols.get(portNumInt) if portNumInt else None # Obtiene el manejador de protocolo para ese puerto/tipo de mensaje

        pb = None
        if handler is not None and handler.protobufFactory is not None:
            pb = handler.protobufFactory()
            pb.ParseFromString(mp.decoded.payload)

        if pb:
            # Clean and update the payload
            pb_str = str(pb).replace('\n', ' ').replace('\r', ' ').strip()
            mp.decoded.payload = pb_str.encode("utf-8")

        from_node = getattr(mp, "from")
        contacto = num_to_id(from_node)

        self.dispositivo.guardarContactos(contacto, "data/contactos.json", from_node)

        contacto = Dispositivo.queContactoEs(from_node, "data/contactos.json")

        if mp.decoded.portnum == 1:
            print("Mensaje recibido de:", contacto)
            print("Mensaje: ", mp.decoded.payload.decode("utf-8"))
            print("\n")
            # Mesaje de texto
            nombreArchivo = "data/mensaje_texto_recibido.json"
            self.dispositivo.guardarDatos(mp.decoded.payload.decode("utf-8"), nombreArchivo)
        
        elif mp.decoded.portnum == 3:
            print("Posicion recibida de:", contacto)
            print("Posicion: ", mp.decoded.payload.decode("utf-8"))
            print("\n")
            # Mesaje de posición GPS
            nombreArchivo = "data/mensaje_posicion_recibido.json"
            self.dispositivo.guardarDatos(mp.decoded.payload.decode("utf-8"), nombreArchivo)

        elif mp.decoded.portnum == 4:
            print("Telemetria recibida de:", contacto)
            print("Telemetria: ", mp.decoded.payload.decode("utf-8"))
            print("\n")
            # Mesaje de telemetria
            nombreArchivo = "data/mensaje_telemetria_recibido.json"
            self.dispositivo.guardarDatos(mp.decoded.payload.decode("utf-8"), nombreArchivo)

        else:
            print("Mensaje de otro tipo recibido de:", contacto)
            print("Mensaje:", mp.decoded.payload.decode("utf-8"))
            print("\n")
            nombreArchivo = "data/mensaje_otro_recibido.json"
            self.dispositivo.guardarDatos(mp.decoded.payload.decode("utf-8"), nombreArchivo)
        
    def decode_encrypted(self, mp):
        # Desencripta el mensaje    
        try:
            key_bytes = base64.b64decode(self.key.encode('ascii'))
            nonce_packet_id = getattr(mp, "id").to_bytes(8, "little")
            nonce_from_node = getattr(mp, "from").to_bytes(8, "little")
            nonce = nonce_packet_id + nonce_from_node
            cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_bytes = decryptor.update(getattr(mp, "encrypted")) + decryptor.finalize()
            data = mesh_pb2.Data()
            data.ParseFromString(decrypted_bytes)
            mp.decoded.CopyFrom(data)
        except Exception as e:
            if self.print_message_packet: print(f"failed to decrypt: \n{mp}")
            if self.debug: print(f"*** Decryption failed: {str(e)}")
            return