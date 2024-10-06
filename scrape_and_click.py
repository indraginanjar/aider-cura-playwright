from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    # Set up the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open the target website
        driver.get("https://katalon-demo-cura.herokuapp.com/")
        
        # Wait for the page to load
        time.sleep(2)

        # Click the "Make Appointment" button
        make_appointment_button = driver.find_element(By.LINK_TEXT, "Make Appointment")
        make_appointment_button.click()

        # Wait for the login page to load
        time.sleep(2)

        # Scrape the login page for demo account credentials
        username = "John Doe"
        password = "ThisIsNotAPassword"

        # Input the username and password
        username_field = driver.find_element(By.ID, "txtUsername")
        password_field = driver.find_element(By.ID, "txtPassword")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the login form
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Wait for a moment to see the result
        time.sleep(5)

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
