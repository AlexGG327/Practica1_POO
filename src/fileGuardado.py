import os
import json
import datetime
import threading
import time

def guardarDatosSensores(nuevo_datos, nombreArchivo):

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

    with open(nombreArchivo, "w", encoding = "utf-8") as archivo:
        json.dump(datosExistentes, archivo, indent = 4, ensure_ascii = False)