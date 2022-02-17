# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pprint import pprint

import requests
from typing import Protocol
from tublatexmaker.services.tub_media_wiki_service import TubMediaWikiService


class DictToText(Protocol):
    def __init__(self):
        ...

    def make_latex(self, dictionary: dict, format_map: dict) -> str:
        ...


class TubToBrill:
    def make_latex(self, dictionary: dict, format_map: dict) -> str:
        return "Hello"


if __name__ == "__main__":
    tubMediaWikiService = TubMediaWikiService(requests)
    query = "[[Category:Title]]|?Title (Arabic)|?Title (transliterated)|limit=5"
    pprint(tubMediaWikiService.semantic_search(query))


def main():
    tubMediaWikiService = TubMediaWikiService(requests)
    query = "[[Category:Title]]|?Title (Arabic)|?Title (transliterated)|limit=5"
    pprint(tubMediaWikiService.semantic_search(query))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
