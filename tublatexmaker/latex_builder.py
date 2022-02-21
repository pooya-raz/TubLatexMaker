"""
latex_builder.py
====================================
A module that creates latex documents
"""


def create_document(list_of_entries: list) -> str:
    """
    Creates a complete latex document

    Parameters
    ---------------------------------
    list_of_entries
        A list that contains all entries from the TUB API.
    """
    latex_of_entries = _create_entries_from_list(list_of_entries)
    monographs_without_commentary = _wrap_monograph_without_commentary(latex_of_entries)
    document = _wrap_document(monographs_without_commentary)
    return document


"""
General Functions
=================

These are functions that act as interfaces.
"""


def _add_pre_and_post_commands(pre: str, latex_body: str, post: str) -> str:
    """Adds the necessary LaTeX commands to text"""
    return pre + latex_body + post


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
    return latex


def _wrap_monograph_without_commentary(latex_body: str) -> str:
    return _add_pre_and_post_commands(
        "\\section{Monographs without commentary}\n\\begin{enumerate}",
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
    \\newfontfamily\\arabicfont[]{Al Bayan}
    \\usepackage{polyglossia}
    \\setmainlanguage{english}
    \\setotherlanguage{arabic}
    \\begin{document}
    """
    post = """
    \\end{document}
    """

    return _add_pre_and_post_commands(pre, latex_body, post)


def _create_dates(entry: dict) -> str:
    death_hijri = _safe_list_get(entry.get("Death (Hijri) text"), 0, "no data")
    death_gregorian = _safe_list_get(entry.get("Death (Gregorian) text"), 0, "no data")
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
    city = manuscript.get("Located in a city", [{"fulltext": "no data"}])[0].get(
        "fulltext"
    )
    manuscript_number = _safe_get(manuscript, "Manuscript number")

    return f"""
    \\item {location}, {city} (\\#{manuscript_number}), dated {year_hijri}/{year_gregorian}
    """


def _make_manuscript_section(list_of_manuscripts: list) -> str:
    if not list_of_manuscripts:
        return "\\textbf{Principle Manuscripts}\n\\newline\nNone\\newline"
    manuscript_section = ""
    for manuscript in list_of_manuscripts:
        manuscript_section += _make_manuscript_entry(manuscript)

    manuscript_section = _add_pre_and_post_commands(
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
        return "\\textbf{Editions}\n\\newline\nNone\\newline"
    edition_section = ""
    for edition in list_of_editions:
        edition_section += make_edition_entry(edition)

    edition_section = _add_pre_and_post_commands(
        "\\textbf{Editions}\n\\begin{itemize}",
        edition_section,
        "\\end{itemize}\n",
    )
    return edition_section


"""
Functions that deal with side-effects
"""


def _create_entries_from_list(list_of_entries: list) -> str:
    result = ""
    for entry in list_of_entries:
        transliterated_title = "".join(entry["Title (transliterated)"])
        arabic_title = entry["Title (Arabic)"][0]
        author = "".join(entry["Has author(s)"][0]["fulltext"])
        description = _safe_list_get(entry.get("Has a description"), 0, "None")
        death_dates = _create_dates(entry)
        manuscripts = entry["manuscripts"]
        editions = entry["editions"]
        result += _make_entry(
            transliterated_title=transliterated_title,
            arabic_title=arabic_title,
            author=author,
            death_dates=death_dates,
            description=description,
            manuscripts=manuscripts,
            editions=editions,
        )
    return result
