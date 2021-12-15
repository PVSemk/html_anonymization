import bs4
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re
import sys
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from urllib.parse import urlparse


class DownloadParseHTML:
    def __init__(self, url, output_folder, page_filename="page", save_media_content=False):
        self.url = url
        self.page_filename = page_filename
        self.output_folder = output_folder
        self.session = requests.Session()
        self.soup = self.get_page()
        self.save_media_content = save_media_content

    def get_page(self):
        response = self.session.get(self.url)
        return BeautifulSoup(response.text, features="lxml")

    def is_url(self, url):
        try:
            result = urlparse(url)
            base_server = urlparse(self.url).netloc
            if all([result.scheme, result.netloc]) and base_server not in result.netloc:
                return True
            else:
                return False
        except ValueError:
            return False

    def save_page(self):
        page_folder = os.path.join(self.output_folder, self.page_filename + "_files")
        if self.save_media_content:
            self.soup_find_and_save(page_folder, 'img', 'src')
            self.soup_find_and_save(page_folder, 'link', 'href')
            self.soup_find_and_save(page_folder, 'script', 'src')
        with open(os.path.join(self.output_folder, self.page_filename + "_original.html"), 'wb') as file:
            file.write(self.soup.prettify('utf-8'))

    def soup_find_and_save(self, page_folder, tag2find="img", inner="src"):
        """saves on specified `pagefolder` all tag2find objects"""
        os.makedirs(page_folder, exist_ok=True)
        for i, res in enumerate(self.soup.findAll(tag2find)):  # images, css, etc..
            try:
                if not res.has_attr(inner):  # check if inner tag (file object) exists
                    continue  # may or may not exist
                if res.has_attr("rel"):
                    if res["rel"][0] == "stylesheet" and self.is_url(res[inner]):
                        continue

                filename, extension = os.path.splitext(os.path.basename(res[inner]))
                filename = re.sub('[^a-zA-Z0-9_].*', '', filename)
                extension = re.sub('[^a-zA-Z].*', '', extension[1:])
                filename = f"{filename}.{extension}"
                fileurl = urljoin(self.url, res.get(inner))
                filepath = os.path.join(page_folder, filename)
                # rename html ref so can move html and folder of files anywhere
                res[inner] = os.path.join(os.path.basename(page_folder), filename)
                if not os.path.isfile(filepath):  # was not downloaded
                    with open(filepath, 'wb') as file:
                        filebin = self.session.get(fileurl)
                        file.write(filebin.content)
            except Exception as exc:
                print(exc, file=sys.stderr)

    def get_soup(self):
        return self.soup


class AnonymizerHTML:
    def __init__(self, soup, output_folder, page_filename="page"):
        self.soup = soup
        self.output_folder = output_folder
        self.analyzer = AnalyzerEngine()
        self.page_filename = page_filename
        self.anonymizer = AnonymizerEngine()

    def anonymize_html_content(self):
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        for t in self.soup.find('html').findAll(text=True, ):
            if type(t) is not bs4.element.NavigableString:
                continue
            text = str(t)
            analyzer_results = analyzer.analyze(text=text,
                                                entities=["PHONE_NUMBER", "PERSON", "LOCATION", "EMAIL_ADDRESS"],
                                                language='en')
            anonymized_text = anonymizer.anonymize(text=text, analyzer_results=analyzer_results,
                                                   operators={"PERSON": OperatorConfig("replace"),
                                                              "PHONE_NUMBER": OperatorConfig("replace"),
                                                              "LOCATION": OperatorConfig("replace"),
                                                              "EMAIL_ADDRESS": OperatorConfig("replace")})
            t.replaceWith(anonymized_text.text)

    def save_anonymized_page(self):
        with open(os.path.join(self.output_folder, self.page_filename + "_anonymized.html"), 'wb') as file:
            file.write(self.soup.prettify('utf-8'))
