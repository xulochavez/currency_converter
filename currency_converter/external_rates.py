import datetime
import requests


def fetch_rates():
    API_KEY = "4d756169850241ad89c79291450af58f"
    URL = f"http://openexchangerates.org/api/latest.json?app_id={API_KEY}"
    r = requests.get(URL)

    if r.status_code == requests.codes.ok:
        response_json = r.json()
        return datetime.datetime.fromtimestamp(response_json['timestamp']), response_json['rates']
    else:
        raise r.raise_for_status()
