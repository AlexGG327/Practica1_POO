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
for i in range(0,len(texto), 128):
    separado.append(texto[i:i+128])  #cogemos desde i hasta i+10 y agregamos

#print(separado)
#print(len(separado))

longitud = len(texto)
tamaño = sys.getsizeof(texto)
print("Tamaño total:", tamaño, "bytes")


"Estado:INICIO_IMAGEN, ID:gatoto, Total_parts:101, Format:jpeg"
"id:gatoto,part:0,data:/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMSEhUTExMWFhUXGBkbGBgYFxgeGxsZHxoYHR0eGxsaHiggGh4lHhoaIjEiJSkrLi4uHSAzODMtNygtLisBCgoKDg0OGxAQGy0lHyUtLS0tLS0tLS0tLS0tLS0tL"
"id:gatoto,part:5,data:yUjl1JLCG4pAEGHGoJrqo2htWGcOz6DoIYweHUuwBIqdf8AdIPPwqkkAKAFy+50jJyEVsuQ7ixg6EAFs0PCWwzHdm0qN4F4KLgMd94lyFQIEJLVL6mwgiZbjZQNYgsh2f0ga8TVnrEO2JoLMmAEPSPT5stLvVorcX"

"Estado:FIN_IMAGEN, ID:gatoto, Total_parts:101, Format:jpeg"

envios = []
def codificar_audio():

    #Primera parte del mensaje
    Estado = "INICIO_AUDIO"
    nombre = input("Nombre del envío: ")
    total_parts = len(separado)
    formato = "mp3"

    primero = {f"Estado":Estado, "ID":nombre, "Total_parts":total_parts, "Format":formato}

    envios.append(primero)

    #Partes intermedias del mensaje
    for i in range(len(separado)):
        id = nombre
        part = i + 1
        data = separado[i]
        #print(f"id:{id},part:{part},data:{data}")
        intermedio = {f"id":id, "part":part, "data":data}
        envios.append(intermedio)

        
    #Ultima parte del mensaje
    Estado_fin = "FIN_AUDIO"
    nombre_fin = nombre
    total_parts_fin = len(separado)
    formato_fin = "mp3"
    ultimo = {f"Estado":Estado_fin, "ID":nombre_fin, "Total_parts":total_parts_fin, "Format":formato_fin}
    envios.append(ultimo)

codificar_audio()

print(envios)

"""
for i in range(len(codificar_audio())):
    print("")
"""