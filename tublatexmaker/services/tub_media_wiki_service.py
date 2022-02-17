import logging
from typing import Protocol, runtime_checkable

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


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