import requests
from dotenv import load_dotenv
import os

class CurrencyConverterAPI:

    def configure():
        load_dotenv()

    def __init__(self):
        self.api_url = os.getenv("api_key")

    def fetch_currencies(self):
        try:
            response = requests.get(self.api_url + "USD", timeout=5)

            if response.status_code == 200:
                data = response.json()
                if "conversion_rates" in data:
                    return data
                else:
                    print("Error: 'rates' key not found in API response!")
                    return None
            else:
                print(f"Error: response status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
