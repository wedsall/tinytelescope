import json
import requests
import os

def download_image(image_url, image_name):
    try:
        response = requests.get(image_url, stream=True)

        if response.status_code == 200:
            # Open a local file with wb (write binary) permission.
            with open(image_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image downloaded successfully: {image_name}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    # Load the JSON data
    with open('all_image_info5.json', 'r') as file:
        data = json.load(file)

    if not os.path.exists('images'):
        os.makedirs('images')  # Create 'images' directory if it doesn't exist

    # Loop through the data
    for item in data:
        full_image_url = item.get('full_image_url')
        image_name = item.get('image_name')
        if full_image_url and image_name:
            download_path = os.path.join('images', image_name)
            download_image(full_image_url, download_path)

if __name__ == "__main__":
    main()

