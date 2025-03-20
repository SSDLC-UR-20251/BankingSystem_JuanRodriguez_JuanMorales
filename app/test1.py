from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Edge()

driver.get("http://127.0.0.1:5000/api/login")
print("[INFO] Página de login cargada.")

driver.find_element(By.ID, "email").send_keys("juanfer.morales@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("Juan1234@")
driver.find_element(By.ID, "Button").click()
print("[INFO] Credenciales enviadas.")

try:
    
    welcome_message_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "welcome_message"))
    )
    welcome_text = welcome_message_element.text
    print(f"[INFO] Mensaje de bienvenida encontrado: {welcome_text}")

    assert "Welcome, Juan Fernando" in welcome_text, "Login fallido: no se encontró el mensaje de bienvenida."

    driver.find_element(By.ID, "logout_button").click()
    
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "Button"))  # Verifica si el botón de login vuelve a estar disponible
    )
    print("[SUCCESS] Logout exitoso.")

except Exception as e:
    print(f"[ERROR] Se produjo un error: {e}")

driver.quit()
