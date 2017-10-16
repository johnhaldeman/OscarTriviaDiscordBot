import unittest

class Test_WikipediaPageController(unittest.TestCase):
    def test_parseOutKeywords(self):
        from WikipediaPageController import WikipediaPageController
        pageController = WikipediaPageController()
        keywords = pageController.parseOutKeywords("https://en.wikipedia.org/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)")

        self.assertTrue('Niffler' in keywords)
        self.assertTrue('Newt Scamander' in keywords)
        self.assertTrue('Eddie Redmayne' in keywords)
        self.assertFalse('Al Pacino' in keywords)


    def test_getAcademyAwardWinners1(self):
        from WikipediaPageController import WikipediaPageController
        pageController = WikipediaPageController()
        films = pageController.getAcademyAwardWinners(0, 0)

        found = False

        for film in films:
            if(film.title == 'Fantastic Beasts and Where to Find Them'):
                found = True
                self.assertEqual(film.year, 2016)
                self.assertEqual(film.numAwards, 1)
                self.assertEqual(film.uri, '/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)')
                self.assertEqual(film.numNominations, 2)

        self.assertTrue(found)



if __name__ == '__main__':
    unittest.main()
