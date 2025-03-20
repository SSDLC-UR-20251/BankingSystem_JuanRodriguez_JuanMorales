from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import re

driver = webdriver.Edge()
driver.get("http://127.0.0.1:5000/api/login")

driver.find_element(By.ID,"email").send_keys("juanfer.morales@urosario.edu.co")
driver.find_element(By.ID,"password").send_keys("Juan1234@")
driver.find_element(By.ID,"Button").click()

time.sleep(2)

welcome_text = driver.find_element(By.ID, "welcome_message").text
assert "Bienvenido" in welcome_text, "Login fallido: no se encontró el mensaje de bienvenida."

driver.find_element(By.ID, "logout_button").click()

time.sleep(2)

driver.quit()
