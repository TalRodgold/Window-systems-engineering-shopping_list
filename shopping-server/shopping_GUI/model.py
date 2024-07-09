import requests
import logging
import json
import logging
from urllib.parse import quote

class Food:
    def __init__(self):
        self.id = None
        self.name = None
        self.price = None

    def requestApi(self, address):
        """Send a GET request to the provided address."""

        try:
            response = requests.get(address, verify=False)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None
        
    def initialize_db(self):
        """Initialize the database with the food items."""
        file_path = "food_list.json"
        foods = self.read_foods_from_file(file_path)
        for food_data in foods:
            name = food_data['name']
            price = food_data['price']
            response = self.post_food(name, price)
            print(response)

    def read_foods_from_file(self, file_path):
        """Read foods data from a JSON file."""
        with open(file_path, 'r') as file:
            return json.load(file)
    
    def post_food(self, name, price):
        """Post a new food item."""
        url = 'https://localhost:7278/api/Food'
        food = Food()
        food.name = name
        food.price = price

        data = {
            'name': food.name,
            'price': food.price
        }

        try:
            response = requests.post(url, json=data, verify=False)
            response.raise_for_status()
            if response.status_code == 201:
                return f"Food '{food.name}' added successfully."
            else:
                return f"Failed to add food '{food.name}': {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return f"Error: {e}"

    def get_all_food(self):
        """Get all food items."""
        url = 'https://localhost:7278/api/Food'
        return self.requestApi(url)
    
    def request_EdamamApi(self, query):
        """Request data from server."""
        
        url = f'https://localhost:7278/api/Recipes/{query}'
        return self.requestApi(url)
    
    def request_ImaggaApi(self, query):
        """Request data from server."""
        
        encoded_query = quote(query, safe='')
        url = f'https://localhost:7278/api/Imagga/{encoded_query}'
        return self.requestApi(url)
    
    def delete_from_db(self, id):
        """Delete food item by ID."""
        
        url = f"https://localhost:7278/api/Food/DeleteById/{id}"
        response = requests.delete(url, verify=False)
        if response.status_code == 204:
            return f"Food with ID {id} deleted successfully."
        elif response.status_code == 404:
            return f"No food found with the specified ID {id} in database."
        else:
            return f"Error occurred: {response.text}"
    
    def update_db(self, id, new_name, new_price):
        """Update food item."""
        print(id, new_name, new_price)
        
        url = f"https://localhost:7278/api/Food/{id}"
        data = {
            'id': id,
            'name': new_name,
            'price': new_price
        }
        headers = {
            'Content-Type': 'application/json'
        }
        print(f"Sending PUT request to {url} with data {data}")  # Debug statement
        try:
            response = requests.put(url, json=data, headers=headers, verify=False)
            response.raise_for_status()
            if response.status_code == 204:
                return f"Food with ID {id} updated successfully."
            elif response.status_code == 404:
                return f"No food found with ID {id}."
            else:
                return f"Failed to update food: {response.status_code} - {response.text}"
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error occurred: {e}")
            return f"Connection error occurred: {e}"
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout error occurred: {e}")
            return f"Timeout error occurred: {e}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return f"Request failed: {e}"

