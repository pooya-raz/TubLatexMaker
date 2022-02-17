from src.tub_latex_converter import to_item_manuscript_with_commentary


def test_title():
    assert "hello" == to_item_manuscript_with_commentary(
        {"title": "Fancy title", "description": "A long description"}
    )
