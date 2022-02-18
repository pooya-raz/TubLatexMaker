import tublatexmaker.tub_latex_converter as convert

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
    assert convert.to_entry_with_commentary(entry_values) == expected
