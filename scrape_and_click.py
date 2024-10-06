from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Set up the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open the target website
        driver.get("https://katalon-demo-cura.herokuapp.com/")
        
        # Wait for the page to load and click the "Make Appointment" button
        make_appointment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Make Appointment"))
        )
        make_appointment_button.click()

        # Wait for the login page to load and scrape the demo account credentials
        username = "John Doe"
        password = "ThisIsNotAPassword"

        # Input the username and password
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtUsername"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtPassword"))
        )
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the login form
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()

        # Wait for a moment to see the result
        WebDriverWait(driver, 10).until(
            EC.url_contains("appointment")
        )

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
