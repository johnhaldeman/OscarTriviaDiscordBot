import unittest

class Test_test1(unittest.TestCase):
    def test_parseOutKeywords(self):
        from WikipediaPageController import WikipediaPageController
        pageController = WikipediaPageController()
        keywords = pageController.parseOutKeywords("https://en.wikipedia.org/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)")

        self.assertTrue('niffler' in keywords)
        self.assertTrue('Newt Scamander' in keywords)
        self.assertTrue('Eddie Redmayne' in keywords)
        self.assertFalse('Al Pacino' in keywords)


if __name__ == '__main__':
    unittest.main()
