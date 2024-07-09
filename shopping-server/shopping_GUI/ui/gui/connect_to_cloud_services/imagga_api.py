from typing import Optional
import requests
import os
import tempfile
from .consts import *

def delete_file(file_path: str):
    try:
        os.remove(file_path)
        print(f"File deleted successfully: {file_path}")
    except Exception as e:
        raise e


def get_imagga(image_path: str) -> list[str]:
    # Opening the image file
    with open(image_path, 'rb') as file:
        # Creating a files dictionary to upload the image
        files = {
            'image': file
        }
        try:
            # Sending POST request to Imagga API
            response = requests.post(IMAGGA_API, files=files, headers=IMAGGA_AUTH_HEADER)

            # Checking if the request was successful
            if response.status_code == 200:
                # Parsing the JSON response
                data = response.json()

                # Extracting tags from the response
                tags = data['result']['tags']

                # Printing the tags
                resault = []
                for tag in tags:
                    if float(tag['confidence']) > IMAGGA_CONFIDENCE:
                        resault.append(tag['tag']['en'])
                return resault
            else:
                raise("Error:", response.status_code, response.text)
        except Exception as e:
            raise e


def download_image(url: str) -> Optional[str]:
    try:
        # Send a GET request to the URL to fetch the image data
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Create the directory if it doesn't exist
        save_dir = TMP_FILE_PATH
        os.makedirs(save_dir, exist_ok=True)

        # Create a temporary file with .jpg extension in the specified directory
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", dir=save_dir, delete=False)
        temp_path = temp_file.name

        # Write the image data to the temporary file
        with open(temp_path, "wb") as file:
            file.write(response.content)

        return temp_path  # Return the path to the downloaded image
    except Exception as e:
        raise e


def check_image(image_url: str):
    try:
        downloaded_image_path = download_image(image_url)
        if downloaded_image_path:
            resault = get_imagga(downloaded_image_path)
            delete_file(downloaded_image_path)
            return resault
        else:
            raise Exception
    except Exception as e:
        raise e