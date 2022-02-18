from pprint import pprint
import requests
from services.tub_media_wiki_service import TubMediaWikiService
from tub_latex_converter import to_entry_with_commentary
from services.file_writer_service import write_to_file
import os.path


def main():
    tub_mediawiki_service = TubMediaWikiService(requests)
    query_monograph_no_commentaries = "[[Category:Title]][[Book type::Monograph]][[Has number of commentaries::0]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)"
    list_of_entries = tub_mediawiki_service.semantic_search(
        query_monograph_no_commentaries
    )
    print(list_of_entries)
    latex_of_entries = [to_entry_with_commentary(entry) for entry in list_of_entries]
    write_to_file("output", "".join(latex_of_entries))


if __name__ == "__main__":
    main()
