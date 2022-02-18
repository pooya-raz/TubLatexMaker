from pprint import pprint
import requests
from services.tub_media_wiki_service import TubMediaWikiService
from tub_latex_converter import to_entry_with_commentary
from services.file_writer_service import write_to_file
import os.path


def main():
    tub_mediawiki_service = TubMediaWikiService(requests)
    query = "[[Category:Title]]|?Title (Arabic)|?Title (transliterated)|limit=5"
    list_of_entries = tub_mediawiki_service.semantic_search(query)
    latex_of_entries = [to_entry_with_commentary(entry) for entry in list_of_entries]
    write_to_file("output", "".join(latex_of_entries))


if __name__ == "__main__":
    main()
