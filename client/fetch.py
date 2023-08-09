import os
import json
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import hashlib
import mimetypes

def fetch_content(url, base_path):
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '')

    file_name = hashlib.md5(url.encode()).hexdigest()+'.json'
    data = {
        'response':{
            'url': response.url,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': base64.b64encode(response.content).decode('utf-8'),
        }
    }

    if 'text/html' in content_type:
        # Fetch HTML content and recursively fetch embedded resources
        soup = BeautifulSoup(response.content, 'html.parser')
        resource_mapping = {}
        for tag in soup.find_all(src=True):
            resource_src = tag.get('src', '')
            print(resource_src)
            if not resource_src:
                continue
            resource_url = urljoin(url, resource_src)
            resource_path = fetch_content(resource_url, base_path)
            resource_mapping[resource_src]=resource_path
            data['resource_mapping'] = resource_mapping
    
    with open(os.path.join(base_path,file_name), 'w') as f:
        json.dump(data, f, indent=4)
    
    return file_name
    
def make_evidence(url, base_path="evidence"):
    os.makedirs(base_path, exist_ok=True)
    entry_file = fetch_content(url, base_path)
    with open(os.path.abspath(os.path.join(base_path,"evidence.json")), 'w') as f:
        data = {
            'entry_file': entry_file,
        }
        json.dump(data, f, indent=4)

def stich_content(file_name, base_path, save_dir):
    with open(os.path.join  (base_path, file_name), 'r') as f:
        data = json.load(f)

    content = base64.b64decode(data['response']['content'])
    content_type = data['response']['headers'].get('Content-Type', '')

    saved_file_extension = mimetypes.guess_extension(content_type.split(';')[0])
    saved_file_name = os.path.splitext(os.path.basename(file_name))[0] + saved_file_extension

    if "text/html" in content_type:
        content = content.decode('utf-8')
        for resource_url, resource_path in data.get('resource_mapping', {}).items():
            # recursively save the embedded resources
            resource_path = stich_content(resource_path, base_path, save_dir)
            # repace all occurences of resource_url with resource_path in content
            content = content.replace(resource_url, resource_path)

        with open(os.path.join(save_dir, saved_file_name), 'w') as f:
            f.write(content)
    else:
        with open(os.path.join(save_dir, saved_file_name), 'wb') as f:
            f.write(content)

    return saved_file_name

def display_evidence(base_path, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(base_path, "evidence.json"), 'r') as f:
        evidence_data = json.load(f)
    
    entry_file = evidence_data['entry_file']
    return stich_content(entry_file, base_path, save_dir) 


def main():
    start_url = 'http://localhost:5000'
    # start_url = "http://localhost:5000/static/Gear-Twitter-Side-navigation-Expanded-Home-gb.jpg"
    # make_evidence(start_url)
    display_entry_file = display_evidence("evidence", "display_evidence")
    print(display_entry_file)

if __name__ == '__main__':
    main()
