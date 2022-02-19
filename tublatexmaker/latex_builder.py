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
) -> str:
    """Makes an entry"""

    return f"""
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
        \\textbf{{Principle manuscripts}}
        \\newline
        This manuscript
        \\newline
        \\newline
        \\textbf{{Editions}}
        \\newline
        This edition.
        \\newline
        \\newline
        \\textbf{{Commentaries}}
        \\newline
        This commentary.
        \\newline
    """


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
    death_hijri = _safe_list_get(entry.get("Death (Hijri) text"), 0, "unknown")
    death_gregorian = _safe_list_get(entry.get("Death (Gregorian) text"), 0, "unknown")
    return f"({death_hijri}/{death_gregorian})"


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
        result += _make_entry(
            transliterated_title=transliterated_title,
            arabic_title=arabic_title,
            author=author,
            death_dates=death_dates,
            description=description,
        )
    return result
