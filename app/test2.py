from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()

driver.get("http://127.0.0.1:5000/api/login")

driver.find_element(By.ID, "email").send_keys("juanfer.morales@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("ContraseñaIncorrecta")
driver.find_element(By.ID, "Button").click()

time.sleep(2)

error_message = driver.find_element(By.ID, "error_message").text

assert "contraseña incorrecta" in error_message.lower(), "Error: No se verificó el mensaje de contraseña fallida."

driver.quit()
