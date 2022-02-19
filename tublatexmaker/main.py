"""
main.py
====================================
The core module that executes the program
"""

import requests
from tublatexmaker.services.tub_media_wiki_service import TubMediaWikiService
from tublatexmaker.latex_builder import *
from tublatexmaker.services.file_writer_service import write_to_file


def main():
    """Executes the program"""
    tub_mediawiki_service = TubMediaWikiService(requests)
    query_monograph_no_commentaries = "[[Category:Title]][[Book type::Monograph]][[Has number of commentaries::0]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)|?Has author(s).Death (Hijri)|?Has author(s).Death (Gregorian)|?Has author(s).Death (Hijri) text|?Has author(s).Death (Gregorian) text|limit=1000"
    list_of_entries = tub_mediawiki_service.semantic_search(
        query_monograph_no_commentaries
    )
    document = create_document(list_of_entries)
    write_to_file("output", document)


if __name__ == "__main__":
    main()
