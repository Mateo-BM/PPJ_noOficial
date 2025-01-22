import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import pandas as pd
from tkcalendar import DateEntry
from reportAYA import reportPPJ

def seleccionar_archivo():
    # Seleccionar un archivo .xls
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xls *.xlsx")]
    )
    if archivo:
        entrada_archivo.delete(0, tk.END)
        entrada_archivo.insert(0, archivo)

def extraer_datos(flag):
    #Obtener valores ingresados
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    archivo = entrada_archivo.get()
    dateFrom = campo_fecha_desde.get_date().strftime("%d/%m/%Y")
    dateUntil = campo_fecha_hasta.get_date().strftime("%d/%m/%Y")
    country = selected_option.get()
    
    try:
        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor, ingresa el usuario y contraseña.")
            return
    
        if not archivo:
            messagebox.showerror("Error", "Por favor, selecciona un archivo Excel.")
            return

        if country == "Selecciona un país":
            messagebox.showerror("Error", "Por favor, selecciona un país.")
            return
        # Leer el archivo Excel
        df = pd.read_excel(archivo)
        
        # Validar si existe la columna "Locales"
        if "Locales" not in df.columns:
            messagebox.showerror("Error", "El archivo seleccionado no contiene una columna 'Locales'.")
            return

        # Extraer los valores de la columna "Locales"
        locales = df["Locales"].dropna().tolist()
        
        # Mostrar los valores extraídos

        reportPPJ(usuario,contrasena,locales,dateFrom,dateUntil,flag,country)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo:\n{e}")
        
        

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Papa John's - Herramienta de generación de reportes (No oficial)")
ventana.geometry("400x500")

# Etiqueta y entrada para usuario
tk.Label(ventana, text="Usuario:").pack(pady=5)
entrada_usuario = tk.Entry(ventana)
entrada_usuario.pack(pady=5)

# Etiqueta y entrada para contraseña
tk.Label(ventana, text="Contraseña:").pack(pady=5)
entrada_contrasena = tk.Entry(ventana, show="*")
entrada_contrasena.pack(pady=5)

# Crear una variable para almacenar la opción seleccionada
selected_option = StringVar()
selected_option.set("Selecciona un país")  # Valor por defecto

# Opciones del dropdown
option = ["Costa Rica", "Guatemala","Selecciona un país"]

# Crear el menú desplegable (dropdown)
dropdown = tk.OptionMenu(ventana, selected_option, *option)
dropdown.pack(pady=20)

# Campos para fechas
tk.Label(ventana, text="Fecha Desde:").pack(pady=5)
campo_fecha_desde = DateEntry(ventana, date_pattern="dd/mm/yyyy")
campo_fecha_desde.pack(pady=5)

tk.Label(ventana, text="Fecha Hasta:").pack(pady=5)
campo_fecha_hasta = DateEntry(ventana, date_pattern="dd/mm/yyyy")
campo_fecha_hasta.pack(pady=5)

# Botón para seleccionar archivo
tk.Label(ventana, text="Archivo Excel:").pack(pady=5)
entrada_archivo = tk.Entry(ventana, width=40)
entrada_archivo.pack(pady=5)
boton_archivo = tk.Button(ventana, text="Seleccionar", command=seleccionar_archivo)
boton_archivo.pack(pady=5)



# Crear un Frame para los botones y colocarlos horizontalmente
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=20)

boton_procesar_ventas = tk.Button(frame_botones, text="Procesar datos Ventas", command=lambda: extraer_datos(1))
boton_procesar_ventas.pack(side="left", padx=10)  # Espacio horizontal entre botones

boton_procesar_mix = tk.Button(frame_botones, text="Procesar datos MIX", command=lambda: extraer_datos(0))
boton_procesar_mix.pack(side="left", padx=10)




# Iniciar el bucle principal de la ventana
ventana.mainloop()