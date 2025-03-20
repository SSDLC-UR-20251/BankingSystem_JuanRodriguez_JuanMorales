from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Edge()

driver.get("http://127.0.0.1:5000/api/login")

driver.find_element(By.ID, "email").send_keys("juanfer.morales@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("ContraseñaIncorrecta")
driver.find_element(By.ID, "Button").click()

try:
    error_message_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "error_message"))
    )
    error_message = error_message_element.text
    print(f"Mensaje de error encontrado: {error_message}")  # Depuración

    assert "Credenciales incorrectas" in error_message, f"Error: Mensaje inesperado '{error_message}'"
    print("Prueba exitosa: Se verificó el mensaje de contraseña fallida.")

except Exception as e:
    print(f"Error: No se verificó el mensaje de contraseña fallida. {e}")

finally:
    driver.quit()
