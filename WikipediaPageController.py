import urllib.request
from bs4 import BeautifulSoup

ACADEMY_AWARD_WINNER_LIST_URI = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

class Film(object):
    """Data Object for a Film"""

    def __init__(self, title,  year, numAwards, numNominations, uri):
        """Construct a Film Object
        tile -- The name of the film
        year -- The year the film was made
        numAwards -- The number of academy awards recieved
        numNominations -- The number of academy award nominations
        uri -- the uri of the Wikipedia entry for the film"""
        self.numAwards = numAwards
        self.year = year
        self.uri = uri
        self.title = title
        self.numNominations = numNominations

    def __repr__(self):
        return ("Title: " + self.title + 
                "\nURI: " + self.uri + 
                "\nYear: " + str(self.year) + 
                "\nTitle: " + self.title  + 
                "\nNumAwards: " + str(self.numAwards) + 
                "\nNumNominations: " + str(self.numNominations))


class WikipediaPageController(object):
    """Used to manage interactions with wikipedia including parsing"""
    def __init__(self):
        pass

    def parseOutKeywords(self, url):
        """Using a wikipedia url, parse and return keywords for a film        
        url -- the url to parse
        """

        f = urllib.request.urlopen(url)
        soup = BeautifulSoup(f, "html.parser")

        keywords = set();

        for header in soup.find_all(['h2']):
            span = header.span
            if span != None and span['id'] in ('Plot', 'Cast'):
                for elem in header.next_siblings:
                    if elem.name and elem.name.startswith('h'):
                        break;
                    elif elem.name:
                        for link in elem.select('a'):
                            text = link.get_text();
                            if not text.startswith('[') and not text == '':
                                keywords.add(text)
        return keywords

    def getStrippedString(self, str):
        """Given a string with special characters in it that appear sometimes in wikipedia, strip the special characters
        string -- The string to strip
        """
        return str.split('(')[0].split('[')[0]

    def parseWinnerFilm(self, filmRow):
        """Given a row from the film table, create a film, populate it, and append to films list
        filmRow -- The BeautifulSoup element for the table row (tr)
        """
        data = filmRow.find_all('td')
        if len(data) > 0:
            anchor = data[0].select('a')[0]
            film = Film(self.getStrippedString(data[0].get_text()),
                        int(self.getStrippedString(data[1].get_text())), 
                        int(self.getStrippedString(data[2].get_text())), 
                        int(self.getStrippedString(data[3].get_text())), 
                        anchor['href'])
            self.films.append(film)

    def parseFilmTable(self, elem):
        """Given the table of Oscar Winners, parse out the list of films and their statistics
        filmRow -- The BeautifulSoup element for the table row (tr)
        """
        filmRows = elem.find_all('tr')
        for filmRow in filmRows:
            self.parseWinnerFilm(filmRow)

    def parseListOfFilms(self, header):
        """Given the the list of films section header, start parsing the list
        header -- The list of films header
        """
        for elem in header.next_siblings:
            if elem.name and elem.name == 'table':
                self.parseFilmTable(elem)

    def getAcademyAwardWinners(self, minNumAwards, afterYear):
        f = urllib.request.urlopen(ACADEMY_AWARD_WINNER_LIST_URI)
        soup = BeautifulSoup(f, "html.parser")
        self.films = list()

        for header in soup.find_all(['h2']):
            span = header.span
            if span != None and span['id'] == 'List_of_films':
                self.parseListOfFilms(header)
        return self.films















