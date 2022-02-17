def to_entry_with_commentary(entry: dict) -> str:
    transliterated_title = "".join(entry["Title (transliterated)"])
    arabic_title = "".join(entry["Title (Arabic)"])
    return f"""
    \\item \\textbf{{{transliterated_title}}}
    {arabic_title}
    \\newline
    Muḥammad b. Faraj al-Ḥimyarī al-Najafī
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


def to_entry(dictionary: dict):
    for entry in dictionary:
        return to_entry_with_commentary(entry)