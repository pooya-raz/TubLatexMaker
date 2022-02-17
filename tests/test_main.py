from src import __version__
from src.tub import title


def test_title():
    assert "\\textbf{title}" == title({"title": "title"})


def test_version():
    assert __version__ == '0.1.0'
