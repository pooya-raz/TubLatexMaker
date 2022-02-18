from pprint import pprint
import requests
from services.tub_media_wiki_service import TubMediaWikiService
from tub_latex_converter import to_entry_with_commentary


def main():
    tub_mediawiki_service = TubMediaWikiService(requests)
    query = "[[Category:Title]]|?Title (Arabic)|?Title (transliterated)|limit=5"
    list_of_entries = tub_mediawiki_service.semantic_search(query)
    latex_of_entries = [to_entry_with_commentary(entry) for entry in list_of_entries]
    pprint("".join(latex_of_entries))


if __name__ == "__main__":
    main()
