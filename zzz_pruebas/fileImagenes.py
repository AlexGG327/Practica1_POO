import base64
from PIL import Image # Asegúrate de tener la biblioteca instalada: pip install Pillow

class PruebaImagen:
    def __init__(self):
        self.cadena_imagen = ""
        self.cadena_base64 = ""

    def imagen_a_cadena(self,ruta_imagen):
        """
        Convierte una imagen a una cadena Base64.
        """
        try:
            with open(ruta_imagen, "rb") as imagen_file:
                # Lee los datos binarios de la imagen
                imagen_bytes = imagen_file.read()
                # Codifica los bytes a Base64
                self.cadena_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
                print(self.cadena_base64)
                return self.cadena_base64
        except FileNotFoundError:
            return "Error: El archivo de imagen no se encontró."
        except Exception as e:
            return f"Ocurrió un error al procesar la imagen: {e}"
    
    def cadena_a_imagen(self,cadena_base64, ruta_salida):
        """
        Convierte una cadena Base64 de vuelta a una imagen y la guarda.
        """
        try:
            # Decodifica la cadena Base64 a bytes
            imagen_bytes = base64.b64decode(cadena_base64)
            # Escribe los bytes en un archivo de imagen
            with open(ruta_salida, "wb") as imagen_file:
                imagen_file.write(imagen_bytes)
            print(f"Imagen guardada en {ruta_salida}")
        except Exception as e:
            print(f"Ocurrió un error al guardar la imagen: {e}")

    # Ejemplo de uso
    # Reemplaza 'tu_imagen.png' con la ruta a tu imagen