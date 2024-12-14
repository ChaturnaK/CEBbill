import subprocess
import sys

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
try:
    import requests
except ImportError:
    print("requests not found. Installing...")
    install("requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup4 not found. Installing...")
    install("beautifulsoup4")

# Now import the libraries
import requests
from bs4 import BeautifulSoup

# Your CEB account number
account_number = "xxxxx"

# URL of the initial form page
form_url = "https://payment.ceb.lk/instantpay"

# Simulate a browser to avoid being blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Start a session
session = requests.Session()

try:
    # Step 1: Get the initial form page
    response = session.get(form_url, headers=headers)
    response.raise_for_status()

    # Step 2: Parse the form to get the dynamic submission URL
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", {"method": "post"})  # Look for the form with POST method
    if form and form.has_attr("action"):
        submit_url = form["action"]
        if not submit_url.startswith("http"):
            # Handle relative URLs
            submit_url = f"https://payment.ceb.lk{submit_url}"

        # Step 3: Prepare the data payload
        data = {"account_no": account_number}

        # Step 4: Submit the form
        post_response = session.post(submit_url, data=data, headers=headers)
        post_response.raise_for_status()

        # Step 5: Parse the response to extract the bill balance
        post_soup = BeautifulSoup(post_response.text, "html.parser")
        balance_element = post_soup.find("div", string="Bill Balance:").find_next_sibling("div")
        if balance_element:
            bill_balance = balance_element.text.strip()
            print(f"Your bill balance is: {bill_balance}")
        else:
            print("Bill balance not found. Check the HTML structure or account number.")
    else:
        print("Form submission URL not found. Check the form structure.")

except Exception as e:
    print(f"An error occurred: {e}")
