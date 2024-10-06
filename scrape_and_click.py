from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re

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

            # Scrape the date format from the placeholder
            date_placeholder = page.get_attribute("input[id='txt_visit_date']", "placeholder")
            date_format = re.search(r'\b(\w{3})\s(\d{1,2}),\s(\d{4})\b', date_placeholder)

            # Set the visit date to next month in the format extracted from the placeholder
            next_month = (datetime.now() + timedelta(days=30))
            formatted_date = next_month.strftime("%b %d, %Y")  # Format as "MMM DD, YYYY"
            page.fill("input[id='txt_visit_date']", formatted_date)

            # Book the appointment
            page.click("button[type='submit']")

            # Wait for the appointment confirmation
            page.wait_for_selector("text='Appointment Confirmation'")

            # Logout from the web
            page.click("text='Logout'")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the browser
            browser.close()

if __name__ == "__main__":
    main()
