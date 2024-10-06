from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

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
            page.wait_for_url("**/appointment**")

            # Select the facility
            page.select_option("select[id='combo_facility']", "Seoul CURA Healthcare Center")

            # Choose Medicaid
            page.check("input[id='radio_program_medicaid']")

            # Set the visit date to next month
            next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            page.fill("input[id='txt_visit_date']", next_month)

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
