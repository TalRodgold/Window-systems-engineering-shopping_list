import requests
import logging
from urllib.parse import quote


def requestApi(address):
        """Send a GET request to the provided address."""

        try:
            response = requests.get(address, verify=False)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None
        

def get_all_food():
        """Get recipe by cookbook name."""

        url = f'https://localhost:7278/api/Food'
        return requestApi(url)
    