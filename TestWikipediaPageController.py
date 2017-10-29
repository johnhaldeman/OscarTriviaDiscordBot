import unittest

class Test_WikipediaPageController(unittest.TestCase):
    def test_parseOutKeywords(self):
        from WikipediaPageController import Film
        film = Film("", 1990, 10, 10, "/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)")
        keywords = film.parseOutKeywords()

        self.assertTrue('Niffler' in keywords[0])
        self.assertTrue('Newt Scamander' in keywords[0])
        self.assertTrue('Eddie Redmayne' in keywords[1])
        self.assertFalse('Tokyo' in keywords[0])
        self.assertFalse('Al Pacino' in keywords[1])


    def test_getAcademyAwardWinners1(self):
        from WikipediaPageController import WikipediaPageController
        pageController = WikipediaPageController()
        films = pageController.getAcademyAwardWinners(0, 0, 9999)

        found = False

        for film in films:
            if(film.title == 'Fantastic Beasts and Where to Find Them'):
                found = True
                self.assertEqual(film.year, 2016)
                self.assertEqual(film.numAwards, 1)
                self.assertEqual(film.uri, '/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)')
                self.assertEqual(film.numNominations, 2)

        self.assertTrue(found)

    def test_getAcademyAwardWinners2(self):
        """ Test to check to see if number of awards criteria works - only 3 films have had 11 awards - Including the third LOTR film
        """
        from WikipediaPageController import WikipediaPageController
        pageController = WikipediaPageController()
        films = pageController.getAcademyAwardWinners(11, 0, 9999)

        found = False

        self.assertEqual(3, len(films))

        for film in films:
            if(film.title == 'The Lord of the Rings: The Return of the King'):
                found = True
                self.assertEqual(film.year, 2003)
                self.assertEqual(film.numAwards, 11)
                self.assertEqual(film.uri, '/wiki/The_Lord_of_the_Rings:_The_Return_of_the_King')
                self.assertEqual(film.numNominations, 11)

        self.assertTrue(found)



if __name__ == '__main__':
    unittest.main()
