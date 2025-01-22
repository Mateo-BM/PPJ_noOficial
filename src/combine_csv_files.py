import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def combine_csv_files(output_folder,flag):
   
    try:
        # Obtener todos los archivos .csv en la carpeta de salida
        csv_files = [f for f in os.listdir(output_folder) if f.endswith('.csv')]
        
        if not csv_files:
            messagebox.showinfo("Información","No hay archivos CSV para combinar.")
            return
        
        # Crear un DataFrame vacío para combinar los datos
        combined_df = pd.DataFrame()

        # Leer y combinar cada archivo CSV
        for file in csv_files:
            file_path = os.path.join(output_folder, file)
            temp_df = pd.read_csv(file_path)
            combined_df = pd.concat([combined_df, temp_df], ignore_index=True)
    
        if flag:
            combined_file_name = f"PPJFinal_Ventas_{datetime.now().strftime('%Y%m%d')}.csv"
            combined_file_path = os.path.join(output_folder, combined_file_name)
            # Fusionar filas duplicadas basadas en 'Tienda', 'Fecha' y 'Canal'
            combined_df = combined_df.groupby(['Tienda', 'Fecha', 'Canal'], as_index=False).first()

            # Completar valores faltantes con datos existentes en las filas duplicadas
            combined_df = combined_df.groupby(['Tienda', 'Fecha', 'Canal'], as_index=False).agg({
                'Cantidad': 'first',
                'Total con Impuesto': 'first',
                'Total Impuesto': 'first'
            })
        
            # Guardar el archivo combinado
            combined_df.to_csv(combined_file_path, index=False)
        
            # Eliminar todos los archivos CSV antiguos excepto el combinado
            for file in csv_files:
                file_path = os.path.join(output_folder, file)
                if os.path.exists(file_path) and file != combined_file_name:
                    os.remove(file_path)
            messagebox.showinfo("Información", "Archivos para ventas combinados correctamente en: " + combined_file_path)
        else:
            
            combined_file_name = f"PPJFinal_MIX_{datetime.now().strftime('%Y%m%d')}.csv"
            combined_file_path = os.path.join(output_folder, combined_file_name)
            # Guardar el archivo combinado
            combined_df.to_csv(combined_file_path, index=False)
        
            # Eliminar todos los archivos CSV antiguos excepto el combinado
            for file in csv_files:
                file_path = os.path.join(output_folder, file)
                if os.path.exists(file_path) and file != combined_file_name:
                    os.remove(file_path)
        
            messagebox.showinfo("Información", "Archivos para datos MIX combinados correctamente en: " + combined_file_path)

    except Exception as e:
        messagebox.showerror("Error","Error al combinar los archivos CSV: " + e)



