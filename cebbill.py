import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
except ImportError:
    install("requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    install("beautifulsoup4")

import requests
from bs4 import BeautifulSoup

account_number = "xxxxx"
form_url = "https://payment.ceb.lk/instantpay"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

session = requests.Session()

try:
    response = session.get(form_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", {"method": "post"})
    if form and form.has_attr("action"):
        submit_url = form["action"]
        if not submit_url.startswith("http"):
            submit_url = f"https://payment.ceb.lk{submit_url}"

        data = {"account_no": account_number}
        post_response = session.post(submit_url, data=data, headers=headers)
        post_response.raise_for_status()

        post_soup = BeautifulSoup(post_response.text, "html.parser")
        balance_element = post_soup.find("div", string="Bill Balance:").find_next_sibling("div")
        if balance_element:
            bill_balance = balance_element.text.strip()
            print(f"Your bill balance is: {bill_balance}")
        else:
            print("Bill balance not found.")
    else:
        print("Form submission URL not found.")

except Exception as e:
    print(f"An error occurred: {e}")
