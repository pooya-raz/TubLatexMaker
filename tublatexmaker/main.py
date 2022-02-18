from pprint import pprint
import requests
from services.tub_media_wiki_service import TubMediaWikiService
from tub_latex_converter import *
from services.file_writer_service import write_to_file
import os.path


def main():
    tub_mediawiki_service = TubMediaWikiService(requests)
    query_monograph_no_commentaries = "[[Category:Title]][[Book type::Monograph]][[Has number of commentaries::0]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)|limit=1000"
    list_of_entries = tub_mediawiki_service.semantic_search(
        query_monograph_no_commentaries
    )
    print(list_of_entries)
    latex_of_entries = "".join(
        [to_entry_with_commentary(entry) for entry in list_of_entries]
    )
    monographs_without_commentary = wrap_monograph_without_commentary(latex_of_entries)
    document = wrap_document(monographs_without_commentary)
    write_to_file("output", document)


if __name__ == "__main__":
    main()
