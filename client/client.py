import os
import json
import requests
import shutil
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
import mimetypes
import re


class EvidenceMaker:
    def __init__(self, base_path="evidence", save_dir="display_evidence"):
        self.visited_urls = set()
        self.base_path = base_path
        self.save_dir = save_dir

    def check_mime_app(self, url):
        """
        Checks if a given URL is a Application MIME.
        If it is then download it and return the file name.
        """
        if url in self.visited_urls or url[:4] != "http":
            return None

        self.visited_urls.add(url)

        response = requests.get(url)
        content_type = response.headers.get("Content-Type", "")

        if not content_type.startswith("application"):
            return None

        file_name = hashlib.md5(url.encode()).hexdigest() + ".json"
        data = {
            "response": {
                "url": response.url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": base64.b64encode(response.content).decode("utf-8"),
            }
        }
        with open(os.path.join(self.base_path, file_name), "w") as f:
            json.dump(data, f, indent=4)

        return file_name

    def fetch_linked_mime_apps(self, soup, url):
        """
        Fetches linked PDFs from a given URL.
        """
        pdf_resource_mapping = {}
        for tag in soup.find_all(lambda tag: tag.name == "a" and tag.has_attr("href")):
            resource_src = tag.get("href", None)
            if not resource_src:
                continue
            resource_url = urljoin(url, resource_src)
            resource_path = self.check_mime_app(resource_url)

            if resource_path is not None:
                pdf_resource_mapping[resource_src] = resource_path

        return pdf_resource_mapping

    def fetch_embedded_resources(self, content, url):
        resource_mapping = {}
        # the BeautifulSoup library for parsing HTML content
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all(
            lambda tag: tag.has_attr("src")
            or tag.has_attr("data-src")
            or (tag.name == "link" and tag.has_attr("href"))
        ):
            resource_src = next(
                (tag[i] for i in ["src", "href", "data-src"] if tag.has_attr(i)), None
            )
            print(resource_src)
            if not resource_src:
                continue
            resource_url = urljoin(url, resource_src)
            if resource_url[:4] != "http" or resource_url in self.visited_urls:
                continue
            resource_path = self.fetch_content(resource_url)
            if resource_path != None:
                resource_mapping[resource_src] = resource_path

        pdf_resource_mapping = self.fetch_linked_mime_apps(soup, url)
        resource_mapping.update(pdf_resource_mapping)
        return resource_mapping

    def fetch_content(self, url):
        """
        Fetches content from a given URL and its embedded resources, storing them in JSON format.
        Returns the file name of the saved JSON.
        """
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)
        response = requests.get(url)
        content_type = response.headers.get("Content-Type", "")

        # generates a unique file name using the MD5 hash of the URL and data saved to a JSON file.
        file_name = hashlib.md5(url.encode()).hexdigest() + ".json"
        data = {
            "response": {
                "url": response.url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": base64.b64encode(response.content).decode("utf-8"),
            }
        }

        if "text/html" in content_type:
            data["resource_mapping"] = self.fetch_embedded_resources(
                response.content, url
            )

        with open(os.path.join(self.base_path, file_name), "w") as f:
            json.dump(data, f, indent=4)

        return file_name

    def make(self, url):
        """
        Creates an evidence file by fetching content and its embedded resources from a URL and saving them.
        """
        os.makedirs(self.base_path, exist_ok=True)
        entry_file = self.fetch_content(url)
        with open(
            os.path.abspath(os.path.join(self.base_path, "evidence.json")), "w"
        ) as f:
            data = {
                "entry_file": entry_file,
            }
            json.dump(data, f, indent=4)

        shutil.make_archive(self.base_path, "zip", self.base_path)
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)


class EvidenceDisplay:
    def __init__(self, base_path="evidence", save_dir="display_evidence"):
        self.base_path = base_path
        self.save_dir = save_dir

    @staticmethod
    def generate_saved_file_name(file_name, content_type):
        """
        Generates a saved file name based on the content type and original file name.
        """
        saved_file_extension = (
            mimetypes.guess_extension(content_type.split(";")[0]) or ".none"
        )
        saved_file_name = (
            os.path.splitext(os.path.basename(file_name))[0] + saved_file_extension
        )
        return saved_file_name

    def process_html_content(self, content, resource_mapping):
        content = content.decode("utf-8")
        for resource_url, resource_path in sorted(
            resource_mapping.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        ):
            # recursively save the embedded resources
            resource_path = self.stich_content(resource_path)
            # repace all occurences of resource_url with resource_path in content
            content = content.replace(resource_url, resource_path)

        content = re.sub(r'(data-)?srcset="(.|\s|\n)*?"', "", content)
        return content

    def stich_content(self, file_name):
        """
        Stitches together content and its embedded resources, saving them in a designated directory.
        """
        with open(os.path.join(self.base_path, file_name), "r") as f:
            data = json.load(f)

        content = base64.b64decode(data["response"]["content"])
        content_type = data["response"]["headers"].get("Content-Type", "")

        saved_file_name = self.generate_saved_file_name(file_name, content_type)

        if "text/html" in content_type:
            resource_mapping = data.get("resource_mapping", {})
            content = self.process_html_content(content, resource_mapping)

            with open(os.path.join(self.save_dir, saved_file_name), "w") as f:
                f.write(content)
        else:
            with open(os.path.join(self.save_dir, saved_file_name), "wb") as f:
                f.write(content)

        return saved_file_name

    def display(self):
        """
        Displays evidence content by stitching and saving resources, returning the file name.
        """
        # load evidence
        os.makedirs(self.save_dir, exist_ok=True)
        shutil.unpack_archive(
            os.path.join(self.base_path + ".zip"), self.base_path, "zip"
        )
        with open(os.path.join(self.base_path, "evidence.json"), "r") as f:
            evidence_data = json.load(f)

        # start from entry file
        entry_file = evidence_data["entry_file"]
        display_entry_file = os.path.abspath(
            os.path.join(self.save_dir, self.stich_content(entry_file))
        )
        # remove directory
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)

        return display_entry_file


def clear():
    dirs = ["evidence", "display_evidence"]
    files = ["evidence.zip"]
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def main():
    clear()
    # start_url = 'https://services.india.gov.in/service/detail/amma-vodi-application-registration-andhra-pradesh'
    # start_url = "http://localhost:5000/static/Gear-Twitter-Side-navigation-Expanded-Home-gb.jpg"
    # start_url = "https://ebird.org/home"
    start_url = "http://localhost:5000"
    evidence_maker = EvidenceMaker()
    evidence_maker.make(start_url)
    evidence_displayer = EvidenceDisplay()
    display_entry_file = evidence_displayer.display()
    print("file://" + display_entry_file)


if __name__ == "__main__":
    main()
