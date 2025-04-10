from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time
import re

# Configuración de opciones para usar el navegador en modo headless
options = Options()
options.add_argument('--headless')  # Ejecutar sin interfaz gráfica
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Crear una instancia de WebDriver utilizando webdriver-manager para gestionar el ChromeDriver automáticamente
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Abrir la URL de la aplicación
driver.get("http://127.0.0.1:5000/api/login")

# Ingresar las credenciales
driver.find_element(By.ID, "email").send_keys("juanfer.morales@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("Juan1234@")
driver.find_element(By.ID, "Button").click()

time.sleep(2)

# Obtener el saldo inicial
saldo_texto = driver.find_element(By.ID, "saldo_usuario").text
saldo_inicial = float(saldo_texto.split(":")[-1].strip())

# Realizar un depósito
driver.find_element(By.ID, "deposit_button").click()
driver.find_element(By.ID, "balance").send_keys("100")
driver.find_element(By.ID, "deposit_button").click()

time.sleep(2)

# Verificar el saldo final
saldo_texto_final = driver.find_element(By.ID, "saldo_usuario").text
saldo_final = float(saldo_texto_final.split(":")[-1].strip())

# Asegurar que el saldo final es el esperado
assert saldo_final == saldo_inicial + 100, f"Error:Saldo no Esperado {saldo_inicial+100},pero se obtuvo {saldo_final}"

# Cerrar el navegador
driver.quit()
