# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import requests
from typing import Protocol
from tub_latex_maker.services.tub_media_wiki_service import TubMediaWikiService


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


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
