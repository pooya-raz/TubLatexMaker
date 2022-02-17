import tublatexmaker.tub_latex_converter as convert

entry = {
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


def test_convert_to_entry():
    entry_values = list(entry.values())[0]["printouts"]
    assert convert.to_entry_with_commentary(entry_values) == "hello"
