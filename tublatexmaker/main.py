"""
main.py
====================================
The core module that executes the program
"""

import requests
from tublatexmaker.services.tub_media_wiki_service import TubMediaWikiService
from tublatexmaker.latex_creater import *
from tublatexmaker.services.file_writer_service import write_to_file


def main():
    """Executes the program"""
    tub_mediawiki_service = TubMediaWikiService(requests)
    document = create_document(tub_mediawiki_service)
    write_to_file("output", document)


if __name__ == "__main__":
    main()
