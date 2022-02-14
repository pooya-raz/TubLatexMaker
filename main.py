# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

import requests
from typing import Protocol


class MediaWikiAPIService(Protocol):
    """Consumes MediaWiki API"""

    def __init__(self):
        ...

    def semantic_search(self, query: str) -> dict:
        ...


class TubMediaWikiService:
    url = "http://144.173.140.108:8080/tub"
    headers = {"user-agent": "my-app/0.0.1"}

    def __init__(self, http_library):
        self.http_library = http_library

    def semantic_search(self, semantic_query: str) -> dict:
        logging.info("Connecting to:" + self.url)
        response = self.http_library.get(
            self.url + "/api.php?action=ask&format=json&query=" + semantic_query,
            headers=self.headers,
        )
        logging.info("Connection status: Successful")
        return response.json()["query"]["results"]


class DictToText(Protocol):
    def __init__(self):
        ...

    def make_latex(self, dictionary: dict, format_map: dict) -> str:
        ...


class TubToBrill:
    def make_latex(self, dictionary: dict, format_map: dict) -> str:
        return "Hello"


class LatexMaker:
    def title(self, dictionary: dict) -> str:
        return "\\textbf{" + dictionary["title"] + "}"


if __name__ == "__main__":
    tubMediaWikiService = TubMediaWikiService(requests)
    query = "[[Category:Title]]|?Title (Arabic)|?Title (transliterated)|limit=5"
    print(tubMediaWikiService.semantic_search(query))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
