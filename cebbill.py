import subprocess
import sys
import requests
from bs4 import BeautifulSoup

def ensure_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"{package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

ensure_package("requests")
ensure_package("bs4")

account_number = "xxxx"

def get_ceb_bill_balance(account_number):
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
        if not form or not form.has_attr("action"):
            raise Exception("Form submission URL not found in the page.")
        submit_url = form["action"]
        if not submit_url.startswith("http"):
            submit_url = f"https://payment.ceb.lk{submit_url}"
        data = {"account_no": account_number}
        post_response = session.post(submit_url, data=data, headers=headers)
        post_response.raise_for_status()
        post_soup = BeautifulSoup(post_response.text, "html.parser")
        balance_element = post_soup.find("div", string="Bill Balance:").find_next_sibling("div")
        if not balance_element:
            raise Exception("Bill balance not found in the response.")
        bill_balance = balance_element.text.strip()
        return f"Your bill balance is: {bill_balance} Rs."
    except requests.exceptions.RequestException as e:
        return f"Network error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    result = get_ceb_bill_balance(account_number)
    print(result)
