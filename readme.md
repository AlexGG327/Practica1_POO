# Práctica 2 Programación por Objetos

Sistema de comunicación por protocolo Meshtastic con interfaz gráfica y manejo de robot turtlebot4 en python.

## Descripción

Esta aplicación permite comunicarse por mensajes por meshtastic con una interfaz gráfica.
Muestra las posiciones recibidas en un mapa de tkintermapview.
Permite manejar un robot turtlebot4 por comandos recibidos por la red meshtastic.

Se compone de distintas clases encargadas de:

  Gestionar la comunicación por MEshtastic (Comunicador)
  Representar los nodos del sistema (Dispositivo)
  Recoger y almacenar datos de sensores por MQTT (ComunicadorSensores)
  Interactuar con la aplicación a través del terminal (InterfazTerminal)

## Configuración

Para configurar cambiar datos en el archivo config.json

## Requisitos

paho-mqtt

meshtastic

cryptography

tkintermapview


Proyecto relalizado por Alejandro Guadalupe García.
