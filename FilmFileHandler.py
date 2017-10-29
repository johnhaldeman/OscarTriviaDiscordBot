
from WikipediaPageController import WikipediaPageController

FILE_NAME = "films.json"

class FilmFileHandler(object):
    
    def __init__(self):
        self.games = dict();
        self.pageController = WikipediaPageController()

    
    def writeSerializedFilms(self, minAwards, minYear, maxYear):
        self.films = self.pageController.getAcademyAwardWinners(minAwards, minYear, maxYear)

        for film in self.films:
            film.parseOutKeywords()

        filmOut = self.pageController.serializeFilmList();

        with open(FILE_NAME, 'w') as f:
            f.write(filmOut)

    def readSerializedFilms(self):
        with open(FILE_NAME, 'r') as f:
            filmin = f.read()
            return self.pageController.deserializeFilmList(filmin)

        


