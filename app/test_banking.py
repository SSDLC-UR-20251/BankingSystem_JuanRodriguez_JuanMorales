from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import re

driver = webdriver.Chrome()
driver = driver.get("https://urban-spoon-qjqppxv46w63g6x-5000.app.github.dev/api/login")

driver.find_element(By.ID,"email").send_keys("juanfer.morales@urosario.edu.co")
driver.find_element(By.ID,"password").send_keys("Juan1234@")
driver.find_element(By.ID,"").click()

time.sleep(2)

saldo_texto = driver.find_element(By.ID,"Saldo Usuario").text
saldo_inicial = float(saldo_texto.split(":")[-1].strip())

driver.find_element(By.ID,"balance").send_keys("100")
driver.find_element(By.ID,"deposit_button").click()

time.sleep(2)

saldo_texto_final = driver.find_element(By.ID,"saldo_usuario").text
saldo_final = float(saldo_texto_final.split(":")[-1].strip())

assert saldo_final == saldo_inicial + 100, f"Error:Saldo no Esperado {saldo_inicial+100},pero se obtuvo {saldo_final}"

driver.quit()
