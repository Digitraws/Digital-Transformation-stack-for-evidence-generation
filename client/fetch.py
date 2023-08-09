import os
import json
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import hashlib

# def get_unique_filename(base_path, filename):
#     index = 1
#     base, ext = os.path.splitext(filename)
#     new_filename = filename
#     while os.path.exists(os.path.join(base_path, new_filename)):
#         new_filename = f"{base} ({index}){ext}"
#         index += 1
#     return new_filename


def fetch_content(url, base_path):
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '')

    if 'image' in content_type:
        file_name = hashlib.md5(url.encode()).hexdigest()+'.json'
        print(os.path.join(base_path,file_name))
        with open(os.path.abspath(os.path.join(base_path,file_name)), 'w') as f:
            data = {
                'response':{
                    'url': response.url,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'content': base64.b64encode(response.content).decode('utf-8'),
                }
            }
            json.dump(data, f, indent=4)
        return file_name

    elif 'text/html' in content_type:
        # Fetch HTML content and recursively fetch embedded resources
        soup = BeautifulSoup(response.content, 'html.parser')
        resource_mapping = {}
        for tag in soup.find_all(['img']):
            resource_url = urljoin(url, tag.get('src', ''))
            resource_path = fetch_content(resource_url, base_path)
            resource_mapping[resource_url]=resource_path

        file_name = hashlib.md5(url.encode()).hexdigest()+'.json'
        with open(os.path.abspath(os.path.join(base_path,file_name)), 'w') as f:
            data = {
                'response':{
                    'url': response.url,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'content': base64.b64encode(response.content).decode('utf-8'),
                },
                'resource_mapping': resource_mapping,
            }
            json.dump(data, f, indent=4)
        return file_name

    else:
        return None

def main():
    start_url = 'http://localhost:5000'
    # start_url = "http://localhost:5000/static/Gear-Twitter-Side-navigation-Expanded-Home-gb.jpg"
    base_path = 'evidence'
    os.makedirs(base_path, exist_ok=True)

    entry_file = fetch_content(start_url, base_path)
    with open(os.path.abspath(os.path.join(base_path,"evidence.json")), 'w') as f:
        data = {
            'entry_file': entry_file,
        }
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
