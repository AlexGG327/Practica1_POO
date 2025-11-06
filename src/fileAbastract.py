class AbstractComunicador:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        pass
    def on_connect(self):
        pass
    def on_message(self):
        pass

class RecibirMensaajesGenerico:
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