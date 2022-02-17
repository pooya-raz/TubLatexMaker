def to_latex(dictionary: dict, key: str, latex_pre: str, latex_post: str) -> str:
    """The basic function that converts to LaTeX"""
    return latex_pre + dictionary[key] + latex_post


# These are implementations of the to_latex function
def title(dictionary: dict) -> str:
    return to_latex(dictionary, "title", "\\textbf{", "}")


def to_title(dictionary: dict) -> str:
    return "\\textbf{" + dictionary["title"] + "}"


def to_author_dates(dictionary: dict) -> str:
    return "hello"


def to_description(dictionary: dict) -> str:
    return "description"


def to_item_manuscript_with_commentary(dictionary: dict) -> str:
    title = to_title(dictionary)
    description = to_description(dictionary)
    return f"""
    \\item {title}
    \\newline
    Muḥammad b. Faraj al-Ḥimyarī al-Najafī
    \\newline
    (1059/1649)
    \\newline
    \\newline
    \\textbf{{Description}}
    {description}
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
