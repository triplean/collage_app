import tkinter as tk
from tkinter import messagebox, Checkbutton, Frame, Canvas, Scrollbar, Button
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import os
import sys

def obtener_ruta_config():
    # Directorio del script principal
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # Si está empaquetado con PyInstaller, ajusta la ruta
    if getattr(sys, 'frozen', False):
        script_dir = sys._MEIPASS

    return os.path.join(script_dir, "config.txt")

def leer_config():
    ruta_config = obtener_ruta_config()

    try:
        with open(ruta_config, 'r') as f:
            contenido = f.read()
            # Puedes hacer algo con el contenido si es necesario
            print("Contenido de config.txt:", contenido)
            return contenido.strip().lower() == 'true'
    except FileNotFoundError:
        print("Archivo config.txt no encontrado en la ubicación:", ruta_config)
        return True  # Valor predeterminado si no se encuentra el archivo

def guardar_config(estado):
    ruta_config = obtener_ruta_config()

    try:
        with open(ruta_config, 'w') as f:
            f.write(str(estado).lower())  # Guardar 'True' o 'False'
    except Exception as e:
        print("Error al guardar en config.txt:", str(e))

def actualizar_config():
    estado = estado_mensaje_var.get()
    guardar_config(estado)
    messagebox.showinfo("Configuración Actualizada", "El archivo config.txt ha sido actualizado.")

def mostrar_mensaje(imagen):
    mensaje = diccionario_mensajes.get(imagen, "Mensaje no disponible")
    ventana_mensaje = tk.Toplevel(root)
    ventana_mensaje.title("Mensaje")
    etiqueta = tk.Label(ventana_mensaje, text=mensaje)
    etiqueta.pack(padx=10, pady=10)

    ventana_mensaje.lift()
    ventana_mensaje.attributes('-topmost', True)
    ventana_mensaje.attributes('-topmost', False)

def abrir_ventana_impresion(url_imagen):
    try:
        webbrowser.open_new_tab(url_imagen)
    except Exception as e:
        mostrar_error("Error al abrir la ventana de impresión", str(e))

def mostrar_ventana_opciones():
    ventana_opciones = tk.Toplevel(root)
    ventana_opciones.title("Opciones")
    ventana_opciones.geometry('300x150')

    def cambiar_estado_mensaje():
        estado = not estado_mensaje_var.get()
        estado_mensaje_var.set(estado)

    # Checkbutton para activar/desactivar el mensaje de inicio
    check_mensaje = Checkbutton(ventana_opciones, text="Mostrar mensaje de inicio", variable=estado_mensaje_var, command=cambiar_estado_mensaje)
    check_mensaje.pack(pady=10)

    # Botón para actualizar la configuración
    btn_actualizar = Button(ventana_opciones, text="Actualizar Configuración", command=actualizar_config)
    btn_actualizar.pack(pady=10)

def mostrar_error(titulo, mensaje):
    messagebox.showerror(titulo, mensaje)

try:
    # Mostrar aviso al inicio
    if leer_config():
        advertencia = "Antes de abrir esta aplicación, asegúrate de haber leído las instrucciones."
        messagebox.showwarning("Advertencia", advertencia)

    root = tk.Tk()
    root.lift()
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
    root.title("Collage")
    root.state('zoomed')

    estado_mensaje_var = tk.BooleanVar(value=leer_config())

    # Diccionario de imágenes y mensajes asociados con URL
    diccionario_mensajes = {
        "https://aaan.annothere.repl.co/collage/img/backyardigans.jpg": "Mensaje 1",
        "https://aaan.annothere.repl.co/collage/img/bob.jpg": "Mensaje 2",
        "https://aaan.annothere.repl.co/collage/img/pinguinos.jpg": "Mensaje 3",
        "https://aaan.annothere.repl.co/collage/img/pocoyo.jpg": "Mensaje 4",
    }

    # Cargar y redimensionar imágenes desde URL
    imagenes_originales = {ruta: Image.open(BytesIO(requests.get(ruta).content)) for ruta in diccionario_mensajes.keys()}
    ancho, alto = 150, 100  # Nuevo tamaño deseado de las imágenes

    imagenes_redimensionadas = {
        ruta: ImageTk.PhotoImage(imagen.resize((ancho, alto))) for ruta, imagen in imagenes_originales.items()
    }

    # Crear barra de menú
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    # Menú Opciones
    barra_menu.add_command(label="Opciones", command=mostrar_ventana_opciones)

    # Menú Imprimir
    barra_menu.add_command(label="Imprimir", command=lambda: abrir_ventana_impresion(url_imagen_a_imprimir))

    # Crear un Frame para contener los botones y la barra de desplazamiento
    frame_contenedor = Frame(root)
    frame_contenedor.pack(expand=True, fill='both')

    # Crear un Canvas para la barra de desplazamiento
    canvas = Canvas(frame_contenedor)
    canvas.pack(side='left', fill='both', expand=True)

    # Crear una barra de desplazamiento vertical
    scrollbar = Scrollbar(frame_contenedor, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    # Configurar el canvas para trabajar con la barra de desplazamiento
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta), "units"))

    # Crear un Frame interior para contener los botones
    frame_botones = Frame(canvas)
    canvas.create_window((0, 0), window=frame_botones, anchor='nw')

    # Inicializar las variables para el control de las columnas
    columna = 0
    fila = 0
    max_botones_por_columna = 3

    # Agregar botones al Frame interior
    for ruta, imagen in imagenes_redimensionadas.items():
        boton = tk.Button(frame_botones, image=imagen, command=lambda ruta=ruta: mostrar_mensaje(ruta), relief='flat', borderwidth=0)
        boton.grid(row=fila, column=columna, padx=10, pady=10)

        # Controlar la disposición de las imágenes
        columna += 1
        if columna > max_botones_por_columna - 1:
            columna = 0
            fila += 1

    # Actualiza la URL real de la imagen a imprimir
    url_imagen_a_imprimir = "https://aaan.annothere.repl.co/collage/impresion.html"

    root.mainloop()

except Exception as e:
    mostrar_error("Error", str(e))