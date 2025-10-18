Práctica 1 Programación por Objetos

Sistema de comunicación por protocolo MQTT y Meshtastic y gestión de datos de sensores a través de MQTT, en python.

Descripción

Esta aplicación permite comunicarse con otros dispositivos, enviar y recibir posiciones en coordenadas, enviar mensajes
directos a contactos guardados anteriormente a través de la red Meshtastic.
Maneja la comunicación con los sensores por MQTT.
Gestiona el almacenamiento de los datos y mensajes y la visualización de estos en el terminal.
Incluye un menú de selección para comunicarse por Meshtastic o recibir datos por MQTT.

Se compone de distintas clases encargadas de:

  Gestionar la comunicación por MEshtastic (Comunicador)
  Representar los nodos del sistema (Dispositivo)
  Recoger y almacenar datos de sensores por MQTT (ComunicadorSensores)
  Interactuar con la aplicación a través del terminal (InterfazTerminal)

Estructura del proyecto

├── main.py
├── requirements.txt
├── static/
│ └── config.json
├── src/
│ ├── fileDispositivo.py
│ ├── fileComunicador.py
│ ├── fileComunicadorSensores.py
│ └── fileInterfaz.py
├── data/
├── contactos.json
├── datosSensores.json
├── mensaje_otro_recibido.json
├── mensaje_posicion_recibido.json
├── mensaje_texto_recibido.json
└── mensaje_telemetria_recibido.json

Ejecución

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Ejecución

python main.py

Configuración

Para configurar cambiar datos en el archivo static/config.json


Requisitos

paho-mqtt
meshtastic
cryptography

Proyecto relalizado por Alejandro Guadalupe García.
