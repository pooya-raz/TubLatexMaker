import logging
from typing import Protocol, runtime_checkable

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


class MediaWikiAPIService(Protocol):
    """Calls a Semantic MediaWiki API"""

    def __init__(self):
        ...

    def semantic_search(self, query: str) -> dict:
        ...


class TubMediaWikiService:
    """
    Calls the TUB Semantic MediaWiki API

    """

    url = "http://144.173.140.108:8080/tub"
    headers = {"user-agent": "my-app/0.0.1"}

    def __init__(self, http_library):
        self.http_library = http_library

    def semantic_search(self, semantic_query: str) -> list:
        logging.info("Connecting to:" + self.url)
        response = self.http_library.get(
            self.url + "/api.php?action=ask&format=json&query=" + semantic_query,
            headers=self.headers,
        )
        logging.info("Connection status: Successful")
        query_results = response.json()["query"]["results"]
        values = list(query_results.values())
        return self.__build_entry(values)
        # return [element["printouts"] for element in values]

    def __build_entry(self, values: list):
        """Build the entry dicts from the response give by the TUB API"""
        list_of_entries = []
        for entry in values:
            x = entry["printouts"]
            x["page_name"] = entry["fulltext"]
            list_of_entries.append(x)
        return list_of_entries

    def get_manuscripts(self, entries: list) -> list:
        list_of_entries = []
        for entry in entries:
            logging.info("Getting manuscript for: " + entry["page_name"])
            query = f"[[Has base text::{entry['page_name']}]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)|?Has author(s).Death (Hijri)|?Has author(s).Death (Gregorian)|?Has author(s).Death (Hijri) text|?Has author(s).Death (Gregorian) text|?Has a description|limit=1000"
            entry["manuscripts"] = self.semantic_search(query)
            list_of_entries.append(entry)
        return list_of_entries
