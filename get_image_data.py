import requests
from bs4 import BeautifulSoup
import json
import os

def get_captions(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find the <h3> tag with the text "Caption"
    h3_caption = soup.find('h3', text='Caption')
    
    captions = []
    if h3_caption:
        # Find all subsequent <p> tags after the <h3>
        for sibling in h3_caption.find_next_siblings():
            if sibling.name == 'p':
                captions.append(sibling.get_text())
            #else:
                # If you want to stop at the first tag that is not a <p>, uncomment the following line
                # break

    return captions

def extract_image_info(url, results):
    result_info = {}

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }

        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            h1_title = soup.find('h1')

            result_info["title"] = h1_title.text.strip() if h1_title else "No title found"

            result_info["paragraphs"] = get_captions(response.text)

            a_tag = soup.find('a', string=lambda text: text and 'Full Res (For Display)' in text)
    
            if a_tag and a_tag.has_attr('href'):
                # Extract the href attribute
                image_url = a_tag.get('href')

                # Check if the URL is absolute or relative
                if image_url.startswith('//'):
                    image_url = 'http:' + image_url  # or 'https:' depending on the protocol required

                image_name = os.path.basename(image_url)
                result_info["image_name"] = image_name

                # If your image URLs are relative, prepend the base URL
                if not image_url.startswith('http'):
                    image_url = "https://webbtelescope.org/" + image_url  # replace with your base URL

                result_info["full_image_url"] = image_url
            else:
                result_info["full_image_url"] = "No 'Fullsize Original' link found"
                result_info["image_name"] = None

            results.append(result_info)  # Append this dictionary to the results list

        else:
            print(f"Failed to retrieve the webpage, status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    results = []  # List to store results from each URL

    with open('webb1-done.txt', 'r') as file:
        for line in file:
            hubble_url = line.strip()
            hubble_url = hubble_url.replace("//", "/")
            if hubble_url:
                print(r"https://webbtelescope.org"+hubble_url)
                extract_image_info("https://webbtelescope.org"+hubble_url,results)

    # Save all results to a single JSON file
    with open('all_image_info-webb.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

if __name__ == "__main__":
    main()

