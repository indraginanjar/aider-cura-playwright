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

        # Wait for a moment to see the result
        time.sleep(5)

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
