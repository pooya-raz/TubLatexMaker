def to_entry_with_commentary(entry: dict) -> str:
    transliterated_title = "".join(entry["Title (transliterated)"])
    arabic_title = entry["Title (Arabic)"][0]
    author = "".join(entry["Has author(s)"][0]["fulltext"])
    return f"""
      \item \\textbf{{{transliterated_title}}}
        \\newline
        \\textarabic{{{arabic_title}}}
        \\newline
        {author}
        \\newline
        (1059/1649)
        \\newline
        \\newline
        \\textbf{{Description}}
        \\newline	
        A short one-line description.
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


def add_pre_and_post_commands(pre: str, latex_body: str, post: str) -> str:
    return pre + latex_body + post


def wrap_monograph_without_commentary(latex_body: str) -> str:
    return add_pre_and_post_commands(
        "\\section{Monographs without commentary}\n\\begin{enumerate}",
        latex_body,
        "\\end{enumerate}",
    )


def wrap_document(latex_body: str) -> str:
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

    return add_pre_and_post_commands(pre, latex_body, post)


def to_entry(dictionary: dict):
    for entry in dictionary:
        return to_entry_with_commentary(entry)
