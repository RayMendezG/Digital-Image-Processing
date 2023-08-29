import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

imagen_original = None
imagen_modificada = None

def ajustar_brillo(imagen, valor_de_brillo):
    img = imagen.copy()
    img = img.astype(np.int16)  # Usamos int16 para evitar desbordamiento
    
    # Aplicar el ajuste de brillo
    img = img + valor_de_brillo
    
    img = np.clip(img, 0, 255)
    img = img.astype(np.uint8)
    return img

def cargar_imagen():
    global imagen_original, imagen_modificada
    file_path = filedialog.askopenfilename()
    if file_path:
        imagen_original = cv2.imread(file_path)
        imagen_modificada = imagen_original.copy()
        mostrar_imagen_modificada(imagen_original)

def mostrar_imagen_original():
    global imagen_modificada, imagen_original
    valor_de_brillo = slider_de_brillo.get()  # Usar el valor del slider
    imagen_modificada = ajustar_brillo(imagen_original, valor_de_brillo)
    mostrar_imagen_modificada(imagen_modificada)
    entrada_de_brillo.delete(0, tk.END)  # Limpiar la entrada
    entrada_de_brillo.insert(0, str(valor_de_brillo))  # Actualizar entrada con valor del slider

def actualizar_desde_slider(event):
    valor_de_brillo = slider_de_brillo.get()
    entrada_de_brillo.delete(0, tk.END)
    entrada_de_brillo.insert(0, str(valor_de_brillo))

def actualizar_desde_teclado(event):
    try:
        valor_de_brillo = float(entrada_de_brillo.get())
        slider_de_brillo.set(valor_de_brillo)
        mostrar_imagen_original()  # Llamar a esta función para actualizar la imagen
    except ValueError:
        pass

# Función mostrar_imagen_modificada actualizada
def mostrar_imagen_modificada(imagen):
    global imagen_modificada
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imagen = Image.fromarray(imagen)

    # Obtener las dimensiones del Canvas
    ancho_de_canvas = image_canvas.winfo_width()
    altura_de_canvas = image_canvas.winfo_height()

    # Obtener las dimensiones originales de la imagen
    anchura_de_img, altura_de_img = imagen.size

    # Calcular las dimensiones finales de la imagen
    if anchura_de_img > ancho_de_canvas or altura_de_img > altura_de_canvas:
        aspect_ratio = anchura_de_img / altura_de_img
        if ancho_de_canvas / altura_de_canvas > aspect_ratio:
            anchura_de_img = ancho_de_canvas
            altura_de_img = int(ancho_de_canvas / aspect_ratio)
        else:
            altura_de_img = altura_de_canvas
            anchura_de_img = int(altura_de_canvas * aspect_ratio)
    else:
        anchura_de_img, altura_de_img = imagen.size

    imagen = imagen.resize((anchura_de_img, altura_de_img), Image.LANCZOS)

    # Calcular las coordenadas para centrar la imagen en el Canvas
    posicion_x = (ancho_de_canvas - anchura_de_img) // 2
    posicion_y = (altura_de_canvas - altura_de_img) // 2

    imagen_modificada = ImageTk.PhotoImage(image=imagen)
    image_canvas.create_image(posicion_x, posicion_y, ancho=tk.NW, image=imagen_modificada)


# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Ajuste de Brillo")
root.geometry(f"{800}x{600}")

# Crear un Canvas como contenedor para la imagen
image_canvas = tk.Canvas(root)
image_canvas.pack(fill=tk.BOTH, expand=True)  # Llena el espacio disponible

# Botón para cargar imagen
boton_de_imagen = tk.Button(root, text="Seleccionar Imagen", command=cargar_imagen)
boton_de_imagen.pack()

# Etiqueta y campo de entrada para el brillo
etiqueta_de_brillo = tk.Label(root, text="Ajustar brillo")
etiqueta_de_brillo.pack()
entrada_de_brillo = tk.Entry(root)
entrada_de_brillo.pack()

# Slider para el brillo
slider_de_brillo = tk.Scale(root, from_=-128, to=128, orient="horizontal", command=actualizar_desde_slider)
slider_de_brillo.pack()

# Asociar actualización desde la entrada
entrada_de_brillo.bind("<FocusOut>", actualizar_desde_teclado)

# Botón para ajustar la imagen
adjust_button = tk.Button(root, text="Ajustar brillo", command=mostrar_imagen_original)
adjust_button.pack()

# Visualización de la imagen
image_label = tk.Label(root)
image_label.pack()

# Obtener el tamaño actual de la ventana y llamar a mostrar_imagen_modificada con una imagen en blanco
root.update_idletasks()  # Asegurar que la ventana esté completamente creada
initial_image = np.zeros((root.winfo_height(), root.winfo_width(), 3), dtype=np.uint8)  # Imagen en blanco
mostrar_imagen_modificada(initial_image)

root.mainloop()
