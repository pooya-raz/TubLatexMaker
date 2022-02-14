import unittest
from main import TubToBrill, LatexMaker


class TestLatex(unittest.TestCase):
    def test_title(self):
        latex_maker = LatexMaker()
        self.assertEqual("\\textbf{title}", latex_maker.title({"title": "title"}))
