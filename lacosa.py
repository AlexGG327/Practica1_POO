import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import time
from meshtastic import BROADCAST_NUM
import paho.mqtt.client as mqtt

from src.fileComunicador import Comunicador
from src.fileComunicadorSensores import ComunicadorSensores
from src.fileDispositivo import Dispositivo


class MeshtasticGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meshtastic MQTT Manager")
        self.root.geometry("900x700")
        
        # Inicializar comunicador
        self.ordenador = Comunicador()
        
        # Cargar configuración
        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
        self.BROKERsensores = config["BROKERsensores"]
        self.mqtt_port = config["mqtt_port"]
        
        # Configurar callbacks MQTT
        self.ordenador.client.on_connect = self.ordenador.on_connect
        self.ordenador.client.on_disconnect = self.ordenador.on_disconnect
        self.ordenador.client.on_message = self.ordenador.on_message
        
        # Cliente para sensores
        self.ordenadorSensores = ComunicadorSensores()
        self.client_sensores = mqtt.Client()
        self.client_sensores.on_connect = self.ordenadorSensores.on_connect
        self.client_sensores.on_message = self.ordenadorSensores.on_message
        
        # Conectar
        self.ordenador.connect_mqtt()
        
        # Variables de estado
        self.escuchando_sensores = False
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Iniciar actualización automática de mensajes
        self.actualizar_mensajes_periodicamente()
        
        # Enviar info de nodo al iniciar
        threading.Thread(target=self.enviar_info_inicial, daemon=True).start()
    
    def enviar_info_inicial(self):
        time.sleep(2)
        self.ordenador.send_node_info(BROADCAST_NUM, want_response=False)
    
    def crear_interfaz(self):
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña 1: Mensajes
        self.crear_pestaña_mensajes()
        
        # Pestaña 2: Posición
        self.crear_pestaña_posicion()
        
        # Pestaña 3: Info de Nodos
        self.crear_pestaña_nodos()
        
        # Pestaña 4: Sensores
        self.crear_pestaña_sensores()
        
        # Pestaña 5: Contactos
        self.crear_pestaña_contactos()
        
        # Barra de estado
        self.crear_barra_estado()
    
    def crear_pestaña_mensajes(self):
        frame_mensajes = ttk.Frame(self.notebook)
        self.notebook.add(frame_mensajes, text="📨 Mensajes")
        
        # Frame superior para visualización
        frame_superior = ttk.LabelFrame(frame_mensajes, text="Mensajes Recibidos", padding=10)
        frame_superior.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_mensajes = scrolledtext.ScrolledText(
            frame_superior, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            font=("Courier", 10)
        )
        self.text_mensajes.pack(fill="both", expand=True)
        self.text_mensajes.config(state="disabled")
        
        # Frame inferior para envío
        frame_inferior = ttk.LabelFrame(frame_mensajes, text="Enviar Mensaje", padding=10)
        frame_inferior.pack(fill="x", padx=10, pady=5)
        
        # Tipo de envío
        frame_tipo = ttk.Frame(frame_inferior)
        frame_tipo.pack(fill="x", pady=5)
        
        ttk.Label(frame_tipo, text="Tipo de envío:").pack(side="left", padx=5)
        self.tipo_envio = tk.StringVar(value="broadcast")
        ttk.Radiobutton(frame_tipo, text="Broadcast", variable=self.tipo_envio, 
                       value="broadcast").pack(side="left", padx=5)
        ttk.Radiobutton(frame_tipo, text="Directo (contacto)", variable=self.tipo_envio, 
                       value="directo").pack(side="left", padx=5)
        
        # Campo de texto
        frame_texto = ttk.Frame(frame_inferior)
        frame_texto.pack(fill="x", pady=5)
        
        ttk.Label(frame_texto, text="Mensaje:").pack(side="left", padx=5)
        self.entry_mensaje = ttk.Entry(frame_texto, width=60)
        self.entry_mensaje.pack(side="left", padx=5, fill="x", expand=True)
        self.entry_mensaje.bind("<Return>", lambda e: self.enviar_mensaje())
        
        # Botón enviar
        ttk.Button(frame_texto, text="Enviar", 
                  command=self.enviar_mensaje).pack(side="left", padx=5)
        
        # Botón limpiar
        ttk.Button(frame_inferior, text="Limpiar Chat", 
                  command=self.limpiar_mensajes).pack(pady=5)
    
    def crear_pestaña_posicion(self):
        frame_posicion = ttk.Frame(self.notebook)
        self.notebook.add(frame_posicion, text="📍 Posición")
        
        frame_principal = ttk.LabelFrame(frame_posicion, text="Enviar Posición GPS", padding=20)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos de entrada
        campos = [
            ("Latitud:", "lat"),
            ("Longitud:", "lon"),
            ("Altitud:", "alt")
        ]
        
        self.entries_posicion = {}
        
        for i, (label_text, key) in enumerate(campos):
            frame = ttk.Frame(frame_principal)
            frame.pack(fill="x", pady=10)
            
            ttk.Label(frame, text=label_text, width=15).pack(side="left", padx=5)
            entry = ttk.Entry(frame, width=30)
            entry.pack(side="left", padx=5)
            
            # Valor actual
            valor_actual = getattr(self.ordenador, key, "")
            entry.insert(0, str(valor_actual))
            self.entries_posicion[key] = entry
            
            ttk.Label(frame, text=f"(Actual: {valor_actual})", 
                     foreground="gray").pack(side="left", padx=5)
        
        # Botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=20)
        
        ttk.Button(frame_botones, text="Enviar Posición", 
                  command=self.enviar_posicion).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Restaurar Valores", 
                  command=self.restaurar_posicion).pack(side="left", padx=5)
    
    def crear_pestaña_nodos(self):
        frame_nodos = ttk.Frame(self.notebook)
        self.notebook.add(frame_nodos, text="🖥️ Nodos")
        
        frame_principal = ttk.LabelFrame(frame_nodos, text="Información de Nodos", padding=20)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información del nodo actual
        info_frame = ttk.LabelFrame(frame_principal, text="Mi Nodo", padding=10)
        info_frame.pack(fill="x", pady=10)
        
        info_text = f"""
Nombre del nodo: {self.ordenador.dispositivo.node_name}
Número del nodo: {self.ordenador.dispositivo.node_number}
Nombre corto: {self.ordenador.client_short_name}
Nombre largo: {self.ordenador.client_long_name}
Modelo hardware: {self.ordenador.client_hw_model}
Canal: {self.ordenador.channel}
        """
        
        ttk.Label(info_frame, text=info_text, justify="left").pack()
        
        # Botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=20)
        
        ttk.Button(frame_botones, text="Enviar Info de Nodo (Broadcast)", 
                  command=self.enviar_info_nodo).pack(pady=5)
        
        ttk.Button(frame_botones, text="Ver Contactos", 
                  command=lambda: self.notebook.select(4)).pack(pady=5)
    
    def crear_pestaña_sensores(self):
        frame_sensores = ttk.Frame(self.notebook)
        self.notebook.add(frame_sensores, text="📊 Sensores")
        
        frame_principal = ttk.LabelFrame(frame_sensores, text="Datos de Sensores", padding=10)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área de visualización
        self.text_sensores = scrolledtext.ScrolledText(
            frame_principal,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Courier", 9)
        )
        self.text_sensores.pack(fill="both", expand=True, pady=5)
        self.text_sensores.config(state="disabled")
        
        # Botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        
        self.btn_sensores = ttk.Button(frame_botones, text="▶️ Iniciar Escucha", 
                                       command=self.toggle_sensores)
        self.btn_sensores.pack(side="left", padx=5)
        
        ttk.Button(frame_botones, text="🗑️ Limpiar", 
                  command=self.limpiar_sensores).pack(side="left", padx=5)
    
    def crear_pestaña_contactos(self):
        frame_contactos = ttk.Frame(self.notebook)
        self.notebook.add(frame_contactos, text="👥 Contactos")
        
        frame_principal = ttk.LabelFrame(frame_contactos, text="Lista de Contactos", padding=10)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview para contactos
        columnas = ("codigo", "numero", "nombre")
        self.tree_contactos = ttk.Treeview(frame_principal, columns=columnas, show="headings")
        
        self.tree_contactos.heading("codigo", text="Código")
        self.tree_contactos.heading("numero", text="Número")
        self.tree_contactos.heading("nombre", text="Nombre")
        
        self.tree_contactos.column("codigo", width=120)
        self.tree_contactos.column("numero", width=150)
        self.tree_contactos.column("nombre", width=200)
        
        self.tree_contactos.pack(fill="both", expand=True, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", 
                                 command=self.tree_contactos.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_contactos.configure(yscrollcommand=scrollbar.set)
        
        # Botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="🔄 Actualizar", 
                  command=self.cargar_contactos).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="✏️ Editar Nombre", 
                  command=self.editar_contacto).pack(side="left", padx=5)
        
        # Cargar contactos inicialmente
        self.cargar_contactos()
    
    def crear_barra_estado(self):
        self.barra_estado = ttk.Label(self.root, text="Estado: Conectado", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Funciones de mensajes
    def enviar_mensaje(self):
        mensaje = self.entry_mensaje.get().strip()
        if not mensaje:
            messagebox.showwarning("Advertencia", "Escribe un mensaje primero")
            return
        
        self.ordenador.message_text = mensaje
        
        if self.tipo_envio.get() == "directo":
            threading.Thread(target=lambda: self.ordenador.send_message(BROADCAST_NUM, True), 
                           daemon=True).start()
        else:
            threading.Thread(target=lambda: self.ordenador.send_message(BROADCAST_NUM, False), 
                           daemon=True).start()
        
        self.agregar_mensaje_enviado(mensaje)
        self.entry_mensaje.delete(0, tk.END)
    
    def agregar_mensaje_enviado(self, mensaje):
        self.text_mensajes.config(state="normal")
        self.text_mensajes.insert(tk.END, f"📤 Enviado: {mensaje}\n\n", "enviado")
        self.text_mensajes.tag_config("enviado", foreground="blue")
        self.text_mensajes.see(tk.END)
        self.text_mensajes.config(state="disabled")
    
    def limpiar_mensajes(self):
        self.text_mensajes.config(state="normal")
        self.text_mensajes.delete(1.0, tk.END)
        self.text_mensajes.config(state="disabled")
        self.ordenador.lista_mensajes_grafica.clear()
    
    def actualizar_mensajes_periodicamente(self):
        # Revisar si hay nuevos mensajes en la lista
        if self.ordenador.lista_mensajes_grafica:
            self.text_mensajes.config(state="normal")
            while self.ordenador.lista_mensajes_grafica:
                mensaje = self.ordenador.lista_mensajes_grafica.pop(0)
                self.text_mensajes.insert(tk.END, f"📥 {mensaje}", "recibido")
            self.text_mensajes.tag_config("recibido", foreground="green")
            self.text_mensajes.see(tk.END)
            self.text_mensajes.config(state="disabled")
        
        # Programar siguiente actualización
        self.root.after(500, self.actualizar_mensajes_periodicamente)
    
    # Funciones de posición
    def enviar_posicion(self):
        # Actualizar valores si han cambiado
        for key, entry in self.entries_posicion.items():
            valor = entry.get().strip()
            if valor:
                setattr(self.ordenador, key, valor)
        
        threading.Thread(target=lambda: self.ordenador.send_position(BROADCAST_NUM), 
                        daemon=True).start()
        
        messagebox.showinfo("Enviado", "Posición GPS enviada correctamente")
    
    def restaurar_posicion(self):
        # Recargar valores desde la configuración
        with open("static/config.json", "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
        
        for key in ["lat", "lon", "alt"]:
            valor = config.get(key, "")
            self.entries_posicion[key].delete(0, tk.END)
            self.entries_posicion[key].insert(0, str(valor))
            setattr(self.ordenador, key, valor)
    
    # Funciones de nodos
    def enviar_info_nodo(self):
        threading.Thread(target=lambda: self.ordenador.send_node_info(BROADCAST_NUM, False), 
                        daemon=True).start()
        messagebox.showinfo("Enviado", "Información de nodo enviada")
    
    # Funciones de sensores
    def toggle_sensores(self):
        if not self.escuchando_sensores:
            self.iniciar_sensores()
        else:
            self.detener_sensores()
    
    def iniciar_sensores(self):
        try:
            self.client_sensores.connect(self.BROKERsensores, self.mqtt_port, 60)
            threading.Thread(target=self.client_sensores.loop_forever, daemon=True).start()
            self.escuchando_sensores = True
            self.btn_sensores.config(text="⏸️ Detener Escucha")
            self.agregar_texto_sensores("📡 Conectado al broker de sensores...\n")
            self.barra_estado.config(text="Estado: Escuchando sensores")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a sensores: {e}")
    
    def detener_sensores(self):
        self.client_sensores.disconnect()
        self.escuchando_sensores = False
        self.btn_sensores.config(text="▶️ Iniciar Escucha")
        self.agregar_texto_sensores("⏹️ Desconectado del broker de sensores\n")
        self.barra_estado.config(text="Estado: Conectado")
    
    def agregar_texto_sensores(self, texto):
        self.text_sensores.config(state="normal")
        self.text_sensores.insert(tk.END, texto)
        self.text_sensores.see(tk.END)
        self.text_sensores.config(state="disabled")
    
    def limpiar_sensores(self):
        self.text_sensores.config(state="normal")
        self.text_sensores.delete(1.0, tk.END)
        self.text_sensores.config(state="disabled")
    
    # Funciones de contactos
    def cargar_contactos(self):
        # Limpiar árbol
        for item in self.tree_contactos.get_children():
            self.tree_contactos.delete(item)
        
        # Cargar desde archivo
        try:
            with open("data/contactos.json", "r", encoding="utf-8") as archivo:
                contactos = json.load(archivo)
                for contacto in contactos:
                    codigo = contacto.get("codigo", "")
                    numero = contacto.get("numero", "")
                    nombre = contacto.get("nombre", "Sin nombre")
                    self.tree_contactos.insert("", tk.END, values=(codigo, numero, nombre))
        except FileNotFoundError:
            messagebox.showinfo("Info", "No hay contactos guardados aún")
    
    def editar_contacto(self):
        seleccion = self.tree_contactos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un contacto primero")
            return
        
        item = self.tree_contactos.item(seleccion[0])
        valores = item['values']
        
        # Ventana de diálogo
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Editar Contacto")
        dialogo.geometry("300x150")
        
        ttk.Label(dialogo, text=f"Código: {valores[0]}").pack(pady=5)
        ttk.Label(dialogo, text=f"Número: {valores[1]}").pack(pady=5)
        
        ttk.Label(dialogo, text="Nuevo nombre:").pack(pady=5)
        entry_nombre = ttk.Entry(dialogo, width=30)
        entry_nombre.pack(pady=5)
        entry_nombre.insert(0, valores[2])
        
        def guardar():
            nuevo_nombre = entry_nombre.get().strip()
            if nuevo_nombre:
                self.actualizar_nombre_contacto(valores[1], nuevo_nombre)
                self.cargar_contactos()
                dialogo.destroy()
        
        ttk.Button(dialogo, text="Guardar", command=guardar).pack(pady=10)
    
    def actualizar_nombre_contacto(self, numero, nuevo_nombre):
        try:
            with open("data/contactos.json", "r", encoding="utf-8") as archivo:
                contactos = json.load(archivo)
            
            for contacto in contactos:
                if contacto["numero"] == numero:
                    contacto["nombre"] = nuevo_nombre
                    break
            
            with open("data/contactos.json", "w", encoding="utf-8") as archivo:
                json.dump(contactos, archivo, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Éxito", "Nombre actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
    
    def cerrar_aplicacion(self):
        if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
            self.ordenador.disconnect_mqtt()
            if self.escuchando_sensores:
                self.client_sensores.disconnect()
            self.root.destroy()


def main():
    root = tk.Tk()
    app = MeshtasticGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()


if __name__ == "__main__":
    main()