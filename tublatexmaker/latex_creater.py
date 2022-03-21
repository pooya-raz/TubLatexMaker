"""
latex_creater.py
====================================
A module that creates latex documents
"""
import json_to_latex_converter


def create_document(mediawiki_service):
    monographs_with_commentaries= create_section("Monographs with commentaries", mediawiki_service)
    monographs_without_commentaries = create_section("Monographs without commentaries", mediawiki_service)
    treatise = create_section("Treatise (risāla)", mediawiki_service)
    commentary = create_section("Commentary (sharḥ)", mediawiki_service)
    gloss = create_section("Gloss (ḥāshīyah)", mediawiki_service)
    marginal_notes = create_section("Marginal notes (taʿlīqa)", mediawiki_service)
    summary = create_section("Summary (khulāṣa/mukhtaṣar)", mediawiki_service)
    poem = create_section("Poem (manẓūma)", mediawiki_service)
    refutation = create_section("Refutation (radd)", mediawiki_service)
    taqrirat = create_section("Taqrīrāt", mediawiki_service)
    translation = create_section(" Translation", mediawiki_service)
    full_text = piece_document_together(
        monographs_with_commentaries
        + monographs_without_commentaries
        + commentary
        + gloss
        + marginal_notes
        + treatise
        + summary
        + poem
        + refutation
        + taqrirat
        + translation
    )
    full_text = full_text.replace(" #", "\\#")
    full_text = full_text.replace("&", "\\&")
    return full_text

def create_section(section_heading: str, mediawiki_service) -> str:
    query =f"[[Category:Title]][[Book type::{section_heading}]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)|?Has author(s).Death (Hijri)|?Has author(s).Death (Gregorian)|?Has author(s).Death (Hijri) text|?Has author(s).Death (Gregorian) text|?Has a catalogue description|limit=10000|sort=Has author(s).Death (Hijri)|order=asc"
    if section_heading == "Monographs without commentaries":
        query = "[[Category:Title]][[Book type::Monograph]][[Has number of commentaries::0]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)|?Has author(s).Death (Hijri)|?Has author(s).Death (Gregorian)|?Has author(s).Death (Hijri) text|?Has author(s).Death (Gregorian) text|?Has a catalogue description|limit=10000|sort=Has author(s).Death (Hijri)|order=asc"
    if section_heading == "Monographs with commentaries":
        query = "[[Category:Title]][[Book type::Monograph]][[Has number of commentaries::>>0]]|?Title (Arabic)|?Title (transliterated)|?Has author(s)|?Has author(s).Death (Hijri)|?Has author(s).Death (Gregorian)|?Has author(s).Death (Hijri) text|?Has author(s).Death (Gregorian) text|?Has a catalogue description|limit=10000|sort=Has author(s).Death (Hijri)|order=asc"

    entries = mediawiki_service.semantic_search(query)
    entries_with_manuscripts = mediawiki_service.get_manuscripts(entries)
    entries_with_manuscripts_and_editions = mediawiki_service.get_editions(entries_with_manuscripts)
    latex_of_entries = _create_entries_from_list(entries_with_manuscripts_and_editions)
    if section_heading == "Monographs with commentaries":
        entries_with_commentaries = mediawiki_service.get_commentaries(entries_with_manuscripts_and_editions)
        latex_of_entries = _create_entries_from_list(entries_with_commentaries)
    return _wrap_section(latex_of_entries, section_heading)


def piece_document_together(latex_body: str) -> str:
    """
    Creates a complete latex document

        :param latex_body:
    """
    document = _wrap_document(latex_body)
    return document


"""
General Functions
=================

These are functions that act as interfaces.
"""


def _safe_list_get(lst: list, index: int, default):
    """Returns a default if index is out of bounds"""
    try:
        return lst[index]
    except IndexError:
        return default


def _safe_get(dictionary: dict, key: str) -> str:
    return _safe_list_get(dictionary.get(key), 0, "no data")


""" 
Implementation functions
========================

Functions that implement the general functions defined above

"""

"""
Pure functions
"""


def _make_entry(
    transliterated_title: str,
    arabic_title: str,
    author: str,
    death_dates: str,
    description: str,
    manuscripts: list,
    editions: list,
    commentaries: list,
) -> str:
    """Makes an entry"""

    latex = f"""
      \item \\textbf{{{transliterated_title}}}
        \\newline
        \\textarabic{{{arabic_title}}}
        \\newline
        {author}
        \\newline
        {death_dates}
        \\newline
        \\newline
        \\textbf{{Description}}
        \\newline	
        {description}
        \\newline
        \\newline
    """
    latex += _make_manuscript_section(manuscripts)
    latex += _make_editions_section(editions)
    if commentaries:
        latex += _make_commentaries_section(commentaries)
    return latex


def _wrap_section(latex_body: str,section_heading: str) -> str:
    return json_to_latex_converter.add_pre_and_post_commands(
        f"\\section{{{section_heading}}}\n\\begin{{enumerate}}",
        latex_body,
        "\\end{enumerate}",
    )




def _wrap_document(latex_body: str) -> str:
    pre = """
    \\documentclass{article}
    \\usepackage{fontspec,lipsum}
    \\defaultfontfeatures{Ligatures=TeX}
    \\usepackage[small,sf,bf]{titlesec}
    \\setromanfont{Gentium Plus}
    \\newfontfamily\\arabicfont[Script=Arabic]{Amiri}
    \\usepackage{polyglossia}
    \\setmainlanguage{english}
    \\setotherlanguage{arabic}
    \\title{Twelver Usul Bibliography}
    \\author{The TUB Team}
    \\date{\\today} 
    \\begin{document}
    \\maketitle
    \\tableofcontents
    \\pagebreak
    """
    post = """
    \\end{document}
    """

    return json_to_latex_converter.add_pre_and_post_commands(pre, latex_body, post)


def _create_dates(entry: dict) -> str:
    death_hijri = "no data"
    death_gregorian = "no data"
    if entry["Death (Hijri)"]:
        death_hijri = entry["Death (Hijri)"][0]
    if entry["Death (Gregorian)"]:
        death_gregorian_raw = entry["Death (Gregorian)"][0].get("raw")
        split_raw = death_gregorian_raw.split("/")
        death_gregorian = split_raw[1]
    if entry["Death (Hijri) text"]:
        death_hijri = entry["Death (Hijri) text"][0]
    if entry["Death (Gregorian) text"]:
        death_gregorian = entry["Death (Gregorian) text"][0]

    return f"({death_hijri}/{death_gregorian})"


def _get_manuscript_gregorian_dates(manuscript: dict) -> str:
    year = _safe_get(manuscript, "Has year(Gregorian) text")
    if year == "no data":
        year = _safe_get(manuscript, "Has year(Gregorian)")
    return year


def _get_manuscript_hijri_dates(manuscript: dict) -> str:
    year = _safe_get(manuscript, "Has year(Hijri) text")
    if year == "no data":
        year = _safe_get(manuscript, "Has year(Hijri)")
    return year


def _make_manuscript_entry(manuscript: dict) -> str:
    location = _safe_get(manuscript, "Has a location")
    year_gregorian = _get_manuscript_gregorian_dates(manuscript)
    year_hijri = _get_manuscript_hijri_dates(manuscript)
    city = _safe_list_get(manuscript.get("Located in a city", [{"fulltext": "no data"}]), 0, {"fulltext": "no data"}).get(
        "fulltext"
    )
    manuscript_number = _safe_get(manuscript, "Manuscript number")

    return f"""
    \\item {location}, {city} (\\#{manuscript_number}), dated {year_hijri}/{year_gregorian}
    """


def _make_manuscript_section(list_of_manuscripts: list) -> str:
    if not list_of_manuscripts:
        return "\\textbf{Principle Manuscripts}\n\\newline\nno data\\newline"
    manuscript_section = ""
    for manuscript in list_of_manuscripts:
        manuscript_section += _make_manuscript_entry(manuscript)

    manuscript_section = json_to_latex_converter.add_pre_and_post_commands(
        "\\textbf{Principle Manuscripts}\n\\begin{itemize}",
        manuscript_section,
        "\\end{itemize}\n",
    )
    return manuscript_section


def _make_editions_section(list_of_editions: list) -> str:
    def make_edition_entry(edition_entry: dict) -> str:
        title = _safe_get(edition_entry, "Title (transliterated)")
        editor = " (ed. " + _safe_get(edition_entry, "Has editor(s)") + ")"
        edition_type = _safe_get(edition_entry, "Edition type")
        publisher = _safe_get(edition_entry, "Has a publisher")
        city = _safe_list_get(
            edition_entry.get("City", [{"fulltext": "no data"}]),
            0,
            {"fulltext": "no data"},
        ).get("fulltext")
        date_gregorian = _get_manuscript_gregorian_dates(edition_entry)
        date_original = _get_manuscript_hijri_dates(edition_entry)
        return f"""
        \\item \\emph{{{title}}}{editor}, {edition_type}, {publisher}, {city}, {date_original}/{date_gregorian}
        """

    if not list_of_editions:
        return "\\textbf{Editions}\n\\newline\nno data\\newline"
    edition_section = ""
    for edition in list_of_editions:
        edition_section += make_edition_entry(edition)

    edition_section = json_to_latex_converter.add_pre_and_post_commands(
        "\\textbf{Editions}\n\\begin{itemize}",
        edition_section,
        "\\end{itemize}\n",
    )
    return edition_section


def _make_commentaries_section(list_of_commentaries: list) -> str:

    def make_commentary_entry(commentary_entry: dict) -> str:
        transliterated_title = "".join(commentary_entry["Title (transliterated)"])
        #arabic_title = _safe_list_get(commentary_entry["Title (Arabic)"], 0, "no data")
        author = "".join(_safe_list_get(commentary_entry["Has author(s)"], 0, {"fulltext": "no data"})["fulltext"])
        #description = _safe_list_get(commentary_entry.get("Has a catalogue description"), 0, "no data")
        death_dates = _create_dates(commentary_entry)
        latex = f"""
              \item \\emph{{{transliterated_title}}}, {author} {death_dates}
            """
        return latex

    commentary_section = ""
    for commentary in list_of_commentaries:
        commentary_section += make_commentary_entry(commentary)

    commentary_section_with_headers = json_to_latex_converter.add_pre_and_post_commands(
        "\\textbf{Commentaries}\n\\begin{itemize}",
        commentary_section,
        "\\end{itemize}\n",
    )
    return commentary_section_with_headers


"""
Functions that deal with side-effects
"""


def _create_entries_from_list(list_of_entries: list) -> str:
    result = ""
    for entry in list_of_entries:
        transliterated_title = "".join(entry["Title (transliterated)"])
        arabic_title = entry["Title (Arabic)"][0]
        author = "".join(_safe_list_get(entry["Has author(s)"], 0, {"fulltext": "no data"})["fulltext"])
        description = _safe_list_get(entry.get("Has a catalogue description"), 0, "no data")
        death_dates = _create_dates(entry)
        manuscripts = entry["manuscripts"]
        editions = entry["editions"]
        commentaries = entry.get("commentaries", [])
        result += _make_entry(
            transliterated_title=transliterated_title,
            arabic_title=arabic_title,
            author=author,
            death_dates=death_dates,
            description=description,
            manuscripts=manuscripts,
            editions=editions,
            commentaries=commentaries,
        )
    return result
