import tkinter as tk
import tkintermapview

"""ventana = tk.Tk()
ventana.title("Hola Tkinter")
ventana.geometry("1100x650")

etiqueta = tk.Label(ventana, text="Hola Mundo")
etiqueta.pack()

ventana.mainloop()"""

def main():
    # create tkinter window
    root_tk = tk.Tk()
    root_tk.geometry(f"{800}x{600}")
    root_tk.title("map_view_example.py")

    # create map widget
    map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # set current widget position and zoom
    map_widget.set_position(42.6863, -2.9476)
    map_widget.set_zoom(15)

    posicion = "latitude_i: 42.68 longitude_i: -2.94 altitude: 0 time: 1763490498"
    lista1 = posicion.split()
    lat = lista1[1]
    lon = lista1[3]
    print(lat, lon)

    map_widget.set_marker(float(lat), float(lon))
    map_widget.set_marker(42.6863, -2.9476, text="Miranda")
    map_widget.set_marker(52.516268, 13.377695, text="Brandenburger Tor")
    root_tk.mainloop()

if __name__ == "__main__":
    main()