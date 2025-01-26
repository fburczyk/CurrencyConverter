import requests


class CurrencyConverterAPI:
    def __init__(self):
        self.api_url = "https://v6.exchangerate-api.com/v6/4131c965c7bf772aafab3b1d/latest/"

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
