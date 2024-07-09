import requests
from functools import reduce
import json
import re
from .consts import *


def get_recepies(items: str) -> list[str]:
    try:
        query_with_items = RECEIPES_QUERYSTRING
        for item in items.split(","):
            query_with_items["q"] += f"\"{item}\", "
            
        # Sending POST request to edamam-recipe-search API
        response = requests.get(RECEIPES_API, headers=RECEIPES_HEADERS, params=query_with_items)

        # Checking if the request was successful
        if response.status_code == 200:
            j = json.loads(response.text)
            resault = []
            for item in j['hits']:
                resault.append(item['recipe']['url'])
            return resault
        else:
            raise ConnectionError("Error:", response.status_code, response.text)
    except Exception as e:
        raise Exception(str(e))

def user_input(unparsed_str: str) -> str:

    try:
        split_list = re.split("[ ,]", unparsed_str)
        for string in split_list:
            if not string.isalpha():
                raise ValueError(f"String '{string}' contains non-letter characters.")
        return reduce(lambda x,y: x + "," + y, split_list) 
    except ValueError as e:
        raise ValueError(f"Error: {e}")

