from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time
import os

BASE_URL = "https://katalon-demo-cura.herokuapp.com/"

# Create a directory for reports with the current datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_directory = f"reports/acp-{timestamp}"
os.makedirs(report_directory, exist_ok=True)

def validate_page(page, expected_elements):
    for element in expected_elements:
        page.wait_for_selector(element)
        print(f"Validated presence of: {element}")

def take_screenshot(page, name):
    screenshot_path = os.path.join(report_directory, f"{name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def generate_html_report():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Screenshot Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ text-align: center; }}
            .screenshot {{ margin: 20px; text-align: center; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>Screenshot Report</h1>
        <div class="screenshots">
    """
    
    # List all screenshots in the report directory
    for filename in os.listdir(report_directory):
        if filename.endswith(".png"):
            html_content += f"""
            <div class="screenshot">
                <h2>{filename}</h2>
                <img src="{report_directory.replace(os.sep, '/')}/{filename}" alt="{filename}">
            </div>
            """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    # Write the HTML content to a file
    report_path = os.path.join(report_directory, "report.html")
    with open(report_path, "w") as report_file:
        report_file.write(html_content)
    print(f"HTML report generated: {report_path}")

def main():
    with sync_playwright() as p:
        # Launch the Chromium browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open the target website
            page.goto(BASE_URL)
            take_screenshot(page, "landing_page")  # Take screenshot of landing page
            validate_page(page, ["text='Make Appointment'"])  # Validate landing page

            # Wait for the "Make Appointment" button and click it
            page.click("text='Make Appointment'")
            take_screenshot(page, "login_page")  # Take screenshot of login page

            # Wait for the username field to be visible
            page.wait_for_selector("input[id='txt-username']")
            validate_page(page, ["input[id='txt-username']", "input[id='txt-password']"])  # Validate login page

            # Scrape the demo account credentials
            username = "John Doe"
            password = "ThisIsNotAPassword"

            # Input the username and password
            page.fill("input[id='txt-username']", username)
            page.fill("input[id='txt-password']", password)

            # Submit the login form
            page.click("button[type='submit']")
            take_screenshot(page, "appointment_page")  # Take screenshot of appointment page

            # Wait for the appointment page to load
            page.wait_for_url(f"{BASE_URL}#appointment")
            validate_page(page, ["select[id='combo_facility']", "button[type='submit']"])  # Validate appointment page

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
            take_screenshot(page, "confirmation_page")  # Take screenshot of confirmation page

            # Wait for the appointment confirmation
            page.wait_for_selector("text='Appointment Confirmation'")
            validate_page(page, ["text='Appointment Confirmation'", "text='Go to Homepage'"])  # Validate confirmation page

            # Scrape the confirmation page to find the side menu toggle button
            side_menu_toggle_selector = "#menu-toggle"  # Update this selector based on the actual confirmation page structure
            page.wait_for_selector(side_menu_toggle_selector)
            page.click(side_menu_toggle_selector)  # Click the side menu toggle button

            # Wait for the logout button to be visible in the side menu
            logout_button_selector = "text='Logout'"  # Update this selector based on the actual confirmation page structure
            page.wait_for_selector(logout_button_selector)
            page.click(logout_button_selector)  # Click the logout button

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the browser
            browser.close()

    # Generate the HTML report after all actions
    generate_html_report()

if __name__ == "__main__":
    main()
