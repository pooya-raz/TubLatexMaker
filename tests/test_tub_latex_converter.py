import tublatexmaker.latex_builder as convert

dict_of_entries = {
    "(Bahth fī) uṣūl al-fiqh": {
        "displaytitle": "",
        "exists": "1",
        "fulltext": "(Bahth fī) uṣūl al-fiqh",
        "fullurl": "http://144.173.140.108:8080/tub/index.php/(Bahth_f%C4%AB)_u%E1%B9%A3%C5%ABl_al-fiqh",
        "namespace": 0,
        "printouts": {
            "Title (Arabic)": ["بحث في) أصول " "الفقه)"],
            "Title (transliterated)": ["(Bahth " "fī) " "uṣūl " "al-fiqh"],
            "Has author(s)": [{"fulltext": "Muḥammad Jawād b. Aḥmad"}],
            "Death (Hijri)": [1299],
            "Death (Gregorian)": [{"timestamp": "-2776982400", "raw": "1/1882"}],
            "Death (Hijri) text": ["13th century"],
            "Death (Gregorian) text": ["19th century"],
        },
    }
}


def create_expected_latex(transliterated_title: str, arabic_title: str) -> str:
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


def test_convert_to_entry():
    entry_values = list(dict_of_entries.values())[0]["printouts"]
    expected = create_expected_latex("(Bahth fī) uṣūl al-fiqh", "بحث في) أصول الفقه)")
    assert convert._make_entry(entry_values) == expected


def test_create_dates():
    entry = {
        "Death (Hijri)": [1299],
        "Death (Gregorian)": [{"timestamp": "-2776982400", "raw": "1/1882"}],
        "Death (Hijri) text": ["13th century"],
        "Death (Gregorian) text": ["19th century"],
    }
    assert convert._create_dates(entry) == "(13th century/19th century)"
