# reportAYA.py

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
from datetime import datetime
from combine_csv_files import combine_csv_files
def reportPPJ(user, password, locales,dateFrom,dateUntil,flag):
    
        
    i = None  # Inicializa una variable para contar las iteraciones
    success = False  # Inicializa una variable para indicar el éxito de la operación
    error_indices = []  # Inicializa una lista para almacenar los índices donde ocurrieron errores

    not_founded_locales  = {
        "Locales": []
    }
    
    chrome_options = Options()
    output_folder = r"C:\output"
    prefs = {
        "download.default_directory": output_folder,   # Carpeta de destino
        "download.prompt_for_download": False,       # No preguntar por descarga
        "download.directory_upgrade": True,          # Actualizar automáticamente el directorio
        "safebrowsing.enabled": True                 # Desactivar advertencias de seguridad
            }
    driver_path = 'C:\PPJReport\Resources\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    
    chrome_options.add_experimental_option("prefs", prefs)
        # Ruta del controlador de Chrome

    chrome_options.add_argument(f"webdriver.chrome.driver={driver_path}")
    # Configuración de las opciones del navegador Chrome

    driver = webdriver.Chrome(options=chrome_options)
    # Inicia una instancia del navegador Chrome

    driver.implicitly_wait(5)
    # Espera implícita

    url = 'https://www.drakeca.com/pj/auth/?error=Usuario+no+autenticado'
    driver.get(url)
    # Abre la URL en el navegador

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loginForm')))
    # Espera explícita hasta que el elemento de inicio de sesión esté presente

    input_usuario = driver.find_element(By.ID, 'username')
    input_contrasena = driver.find_element(By.ID, 'password')
    # Encuentra los elementos de entrada de usuario y contraseña

    input_usuario.clear()
    input_usuario.send_keys(user)
    input_contrasena.clear()
    input_contrasena.send_keys(password)
    # Ingresa el usuario y la contraseña

    time.sleep(2)  # Espera un tiempo

    boton_submit = driver.find_element(By.ID, 'submit')
    driver.execute_script("arguments[0].click();", boton_submit)
    # Hace clic en el botón de inicio de sesión
    try:
        if flag:

            

            time.sleep(3)  # Espera un tiempo

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/pj/app/inicio.php?op=menu1&cy=GT&co=PJ']")))
            # Espera explícita hasta que aparezca el menú de addons

            tab_start = driver.find_element(By.XPATH, "//a[@href='/pj/app/inicio.php?op=menu1&cy=GT&co=PJ']")
            tab_start.click()

            # Navega a la pestaña donde se encuentran los reportes

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'reporte.php?op=menu&cy=GT&co=PJ')]")))
            tab_report = driver.find_element(By.XPATH, "//a[contains(@href, 'reporte.php?op=menu&cy=GT&co=PJ')]")
            tab_report.click()

            # Navega a la pestaña donde se encuentran los productos


            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='VENTAS POR CANAL']")))
            tab_product = driver.find_element(By.XPATH, "//a[text()='VENTAS POR CANAL']")
            tab_product.click()

            # Configuración del rango de fechas
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'DocDate1')))
            driver.find_element(By.ID, 'DocDate1').clear()
            driver.find_element(By.ID, 'DocDate1').send_keys(dateFrom)
            driver.find_element(By.ID, 'DocDate2').clear()
            driver.find_element(By.ID, 'DocDate2').send_keys(dateUntil)


            # Iterar sobre los locales
            for i_Ventas, local_Ventas in enumerate(locales):
                try:
                    # Seleccionar el local en el dropdown
                    select_tienda = Select(driver.find_element(By.ID, 'Tienda'))
                    select_tienda.select_by_visible_text(local_Ventas)

                    # Generar el reporte
                    Button_Report= driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
                    Button_Report.click()
                    if i_Ventas == len(locales) - 1:
                        time.sleep(2)

                except Exception as e:
                    print(f"No se encontró el local: {local_Ventas}. Error: {e}")
                    not_founded_locales.append(local_Ventas)
                
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='../app/reporte.php?op=menu&cy=GT&co=PJ']")))
            # Espera explícita hasta que aparezca el menú de addons

            tab_start = driver.find_element(By.XPATH, "//a[@href='../app/reporte.php?op=menu&cy=GT&co=PJ']")
            tab_start.click()        
                
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='TRANSACCIONES POR CANAL']")))
            tab_product = driver.find_element(By.XPATH, "//a[text()='TRANSACCIONES POR CANAL']")
            tab_product.click()

            # Configuración del rango de fechas
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'DocDate1')))
            driver.find_element(By.ID, 'DocDate1').clear()
            driver.find_element(By.ID, 'DocDate1').send_keys(dateFrom)
            driver.find_element(By.ID, 'DocDate2').clear()
            driver.find_element(By.ID, 'DocDate2').send_keys(dateUntil)
        
            for i_Canal, local_Canal in enumerate(locales):
                try:
                    # Seleccionar el local en el dropdown
                    select_tienda = Select(driver.find_element(By.ID, 'Tienda'))
                    select_tienda.select_by_visible_text(local_Canal)

                    # Generar el reporte
                    Button_Report= driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
                    Button_Report.click()
                    if i_Canal == len(locales) - 1:
                        time.sleep(2)

                except Exception as e:
                    print(f"No se encontró el local: {local_Canal}. Error: {e}")
                    not_founded_locales.append(local_Canal)

                    print(f"Locales no encontrados: {not_founded_locales}")
            combine_csv_files(output_folder,1)
        else:
            time.sleep(3)  # Espera un tiempo

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/pj/app/inicio.php?op=menu1&cy=GT&co=PJ']")))
            # Espera explícita hasta que aparezca el menú de addons

            tab_start = driver.find_element(By.XPATH, "//a[@href='/pj/app/inicio.php?op=menu1&cy=GT&co=PJ']")
            tab_start.click()

            # Navega a la pestaña donde se encuentran los reportes

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'reporte.php?op=menu&cy=GT&co=PJ')]")))
            tab_report = driver.find_element(By.XPATH, "//a[contains(@href, 'reporte.php?op=menu&cy=GT&co=PJ')]")
            tab_report.click()

            # Navega a la pestaña donde se encuentran los productos


            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='PRODUCTO']")))
            tab_product = driver.find_element(By.XPATH, "//a[text()='PRODUCTO']")
            tab_product.click()

            # Configuración del rango de fechas
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'DocDate1')))
            driver.find_element(By.ID, 'DocDate1').clear()
            driver.find_element(By.ID, 'DocDate1').send_keys(dateFrom)
            driver.find_element(By.ID, 'DocDate2').clear()
            driver.find_element(By.ID, 'DocDate2').send_keys(dateUntil)


            # Iterar sobre los locales
            for i, local in enumerate(locales):
                try:
                    # Seleccionar el local en el dropdown
                    select_tienda = Select(driver.find_element(By.ID, 'Tienda'))
                    select_tienda.select_by_visible_text(local)

                    # Generar el reporte
                    Button_Report= driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
                    Button_Report.click()
                    if i == len(locales) - 1:
                        time.sleep(2)

                except Exception as e:
                    print(f"No se encontró el local: {local}. Error: {e}")
                    not_founded_locales.append(local)
                
                    print(f"Locales no encontrados: {not_founded_locales}") 
            combine_csv_files(output_folder,0)    
        
                
    except Exception as e:
        print(f"Ocurrió un error en el proceso: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

    return not_founded_locales


    
