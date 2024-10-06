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
    validation_results = []
    for element in expected_elements:
        try:
            page.wait_for_selector(element)
            validation_results.append((f"Validated presence of: {element}", "Pass", ""))
        except Exception:
            validation_results.append((f"Validated presence of: {element}", "Fail", ""))
    return validation_results

def take_screenshot(page, name):
    screenshot_path = os.path.join(report_directory, f"{name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def generate_html_report(steps, validation_results):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aider Cura Playwright</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ text-align: center; }}
            .screenshot {{ margin: 20px; text-align: center; }}
            img {{ max-width: 100%; height: auto; }}
            .steps {{ margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Screenshot Report</h1>
        <div class="steps">
            <h2>Steps</h2>
            <ul>
    """
    
    # Add each step to the summary
    for step in steps:
        html_content += f"<li>{step}</li>"
    
    html_content += """
            </ul>
        </div>
        <div class="validation-results">
            <h2>Validation Results</h2>
            <table>
                <tr>
                    <th>Validation Description</th>
                    <th>Pass</th>
                    <th>Fail</th>
                </tr>
    """
    
    # Add each validation result to the report
    for result in validation_results:
        description, status, _ = result
        pass_status = "✔" if status == "Pass" else ""
        fail_status = "✖" if status == "Fail" else ""
        html_content += f"""
                <tr>
                    <td>{description}</td>
                    <td>{pass_status}</td>
                    <td>{fail_status}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
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
    steps = []  # List to hold the steps taken during execution
    validation_results = []  # List to hold validation results
    with sync_playwright() as p:
        # Launch the Chromium browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open the target website
            page.goto(BASE_URL)
            steps.append("Opened the landing page.")
            take_screenshot(page, "landing_page")  # Take screenshot of landing page
            validation_results.extend(validate_page(page, ["text='Make Appointment'"]))  # Validate landing page
            steps.append("Validated landing page.")

            # Wait for the "Make Appointment" button and click it
            page.click("text='Make Appointment'")
            steps.append("Clicked on 'Make Appointment'.")
            take_screenshot(page, "login_page")  # Take screenshot of login page

            # Wait for the username field to be visible
            page.wait_for_selector("input[id='txt-username']")
            validation_results.extend(validate_page(page, ["input[id='txt-username']", "input[id='txt-password']"]))  # Validate login page
            steps.append("Validated login page.")

            # Scrape the demo account credentials
            username = "John Doe"
            password = "ThisIsNotAPassword"

            # Input the username and password
            page.fill("input[id='txt-username']", username)
            page.fill("input[id='txt-password']", password)
            steps.append("Entered username and password.")

            # Submit the login form
            page.click("button[type='submit']")
            steps.append("Submitted the login form.")
            take_screenshot(page, "appointment_page")  # Take screenshot of appointment page

            # Wait for the appointment page to load
            page.wait_for_url(f"{BASE_URL}#appointment")
            validation_results.extend(validate_page(page, ["select[id='combo_facility']", "button[type='submit']"]))  # Validate appointment page
            steps.append("Validated appointment page.")

            # Select the facility
            page.select_option("select[id='combo_facility']", "Seoul CURA Healthcare Center")
            steps.append("Selected the facility.")

            # Choose Medicaid
            page.check("input[value='Medicaid']")
            steps.append("Chose Medicaid.")

            # Set the visit date to next month in the format dd/mm/yyyy
            next_month = (datetime.now() + timedelta(days=30))
            formatted_date = next_month.strftime("%d/%m/%Y")  # Format as "DD/MM/YYYY"

            # Press the key sequence to input the date
            date_input_selector = "input[id='txt_visit_date']"
            page.click(date_input_selector)  # Click to focus on the input field
            time.sleep(1)  # Wait for a moment to ensure the field is focused
            page.keyboard.type(formatted_date)  # Type the formatted date
            steps.append(f"Set the visit date to {formatted_date}.")

            # Book the appointment
            page.click("button[type='submit']")
            steps.append("Booked the appointment.")
            take_screenshot(page, "confirmation_page")  # Take screenshot of confirmation page

            # Wait for the appointment confirmation
            page.wait_for_selector("text='Appointment Confirmation'")
            validation_results.extend(validate_page(page, ["text='Appointment Confirmation'", "text='Go to Homepage'"]))  # Validate confirmation page
            steps.append("Validated confirmation page.")

            # Scrape the confirmation page to find the side menu toggle button
            side_menu_toggle_selector = "#menu-toggle"  # Update this selector based on the actual confirmation page structure
            page.wait_for_selector(side_menu_toggle_selector)
            page.click(side_menu_toggle_selector)  # Click the side menu toggle button

            # Wait for the logout button to be visible in the side menu
            logout_button_selector = "text='Logout'"  # Update this selector based on the actual confirmation page structure
            page.wait_for_selector(logout_button_selector)
            page.click(logout_button_selector)  # Click the logout button
            steps.append("Logged out.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the browser
            browser.close()

    # Generate the HTML report after all actions
    generate_html_report(steps, validation_results)

if __name__ == "__main__":
    main()
