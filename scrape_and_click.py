from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re
import time

def main():
    with sync_playwright() as p:
        # Launch the Chromium browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open the target website
            page.goto("https://katalon-demo-cura.herokuapp.com/")
            
            # Wait for the "Make Appointment" button and click it
            page.wait_for_selector("text='Make Appointment'")
            page.click("text='Make Appointment'")

            # Wait for the username field to be visible
            page.wait_for_selector("input[id='txt-username']")

            # Scrape the demo account credentials
            username = "John Doe"
            password = "ThisIsNotAPassword"

            # Input the username and password
            page.fill("input[id='txt-username']", username)
            page.fill("input[id='txt-password']", password)

            # Submit the login form
            page.click("button[type='submit']")

            # Wait for the appointment page to load
            page.wait_for_url("https://katalon-demo-cura.herokuapp.com/#appointment")

            # Select the facility
            page.select_option("select[id='combo_facility']", "Seoul CURA Healthcare Center")

            # Choose Medicaid
            page.check("input[value='Medicaid']")

            # Set the visit date to next month in the format dd/mm/yyyy
            next_month = (datetime.now() + timedelta(days=30))
            formatted_date = next_month.strftime("%d/%m/%Y")  # Format as "DD/MM/YYYY"

            # Press the key sequence to input the date
            date_input_selector = "input[id='txt_visit_date']"
            page.click(date_input_selector)  # Click to focus on the input field
            time.sleep(1)  # Wait for a moment to ensure the field is focused
            page.keyboard.type(formatted_date)  # Type the formatted date

            # Book the appointment
            page.click("button[type='submit']")

            # Wait for the appointment confirmation
            page.wait_for_selector("text='Appointment Confirmation'")

            # Scrape the confirmation page to find the logout button
            logout_button_selector = "a[href='https://katalon-demo-cura.herokuapp.com/#']"  # Update this selector based on the actual confirmation page structure
            page.wait_for_selector(logout_button_selector)
            page.click(logout_button_selector)  # Click the logout button

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the browser
            browser.close()

if __name__ == "__main__":
    main()
