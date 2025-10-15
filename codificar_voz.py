import base64
import requests
import sys

with open("voz.mp3", 'rb') as audio:
    audio_codificado = base64.b64encode(audio.read())

#print(audio_codificado)

with open("voz_codificada.txt", 'wb') as archivo_salida_string:
    archivo_salida_string.write(audio_codificado)

"""
with open("voz_codificada.txt", "rb") as archivo_entrada:
    audio_b64 = archivo_entrada.read()

audio_bytes = base64.b64decode(audio_b64)

with open("voz_decodificada.mp3", "wb") as archivo_salida_voz:
    archivo_salida_voz.write(audio_bytes)
"""

texto = audio_codificado
separado = [] #aqui se guardará cada pedazo

#indicamos que se repita segun el tamaño de la cadena y que vaya de 10 en 10
for i in range(0,len(texto), 100):
    separado.append(texto[i:i+100])  #cogemos desde i hasta i+10 y agregamos

print(separado)

longitud = len(texto)
tamaño = sys.getsizeof(texto)
print("Tamaño total:", tamaño, "bytes")