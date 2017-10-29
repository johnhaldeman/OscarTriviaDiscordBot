import urllib.request
import json
import collections
from bs4 import BeautifulSoup

ACADEMY_AWARD_WINNER_LIST_URI = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

class Film(object):
    """Data Object for a Film"""

    def __init__(self, title,  year, numAwards, numNominations, uri, **keywords):
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
        if ('keywordSetList' in keywords):
            self.keywordSetList = keywords['keywordSetList']


    def parseOutKeywords(self):
        """Using a wikipedia url, parse and return keywords for a film        
        url -- the url to parse
        """

        f = urllib.request.urlopen("https://en.wikipedia.org" + self.uri)
        soup = BeautifulSoup(f, "html.parser")

        keywordSetList = list()

        for header in soup.find_all(['h2']):
            span = header.span
            if span != None and span['id'] in ('Plot', 'Cast'):
                keywords = set();
                for elem in header.next_siblings:
                    if elem.name and elem.name == 'h2':
                        break;
                    elif elem.name:
                        for link in elem.select('a'):
                            text = link.get_text();
                            if not text.startswith('[') and not text == '':
                                keywords.add(text)
                keywordSetList.append(keywords)
        self.keywordSetList = keywordSetList
        return keywordSetList


    def __repr__(self):
        retString = (
            "Title: " + self.title + 
                "\nURI: " + self.uri + 
                "\nYear: " + str(self.year) + 
                "\nTitle: " + self.title  + 
                "\nNumAwards: " + str(self.numAwards) + 
                "\nNumNominations: " + str(self.numNominations)
        )
        try:
            if(len(self.keywordSetList) > 0):
                retString += "\nPlotKeywords: " + ','.join(self.keywordSetList[0])
            if(len(self.keywordSetList) > 1):
                retString += "\nCastKeywords: " + ','.join(self.keywordSetList[1])
        except AttributeError:
            pass
        return retString


class WikipediaPageController(object):
    """Used to manage interactions with wikipedia including parsing"""
    def __init__(self):
        pass

    def serializeFilmList(self):
        def defaultHandler(obj):
            if isinstance(obj, collections.Set):
                return list(obj)
            else:
                return obj.__dict__
        return json.dumps(self.films, default=defaultHandler)

    def deserializeFilmList(self, str):
        def asFilms(filmDict):
            if 'keywordSetList' in filmDict:
                film = Film(filmDict['title'], filmDict['year'], filmDict['numAwards'], filmDict['numNominations'], filmDict['uri'], keywordSetList=filmDict['keywordSetList'])
            else:
                film = Film(filmDict['title'], filmDict['year'], filmDict['numAwards'], filmDict['numNominations'], filmDict['uri'])
            return film

        self.films = json.loads(str, object_hook = asFilms)
        return self.films


    def getStrippedString(self, str):
        """Given a string with special characters in it that appear sometimes in wikipedia, strip the special characters
        string -- The string to strip
        """
        return str.split('(')[0].split('[')[0]

    def parseWinnerFilm(self, filmRow, minNumAwards, afterYear, beforeYear):
        """Given a row from the film table, create a film, populate it, and append to films list
        filmRow -- The BeautifulSoup element for the table row (tr)
        """
        data = filmRow.find_all('td')
        if len(data) > 0:
            numAwards = int(self.getStrippedString(data[2].get_text()))
            year = int(self.getStrippedString(data[1].get_text()))
            anchor = data[0].select('a')[0]
            title = self.getStrippedString(data[0].select('a')[0]['title']).strip()

            if year >= afterYear and year <= beforeYear and numAwards >= minNumAwards :
                film = Film(title,
                            year, 
                            numAwards, 
                            int(self.getStrippedString(data[3].get_text())), 
                            anchor['href'])
                self.films.append(film)

    def parseFilmTable(self, elem, minNumAwards, afterYear, beforeYear):
        """Given the table of Oscar Winners, parse out the list of films and their statistics
        filmRow -- The BeautifulSoup element for the table row (tr)
        """
        filmRows = elem.find_all('tr')
        for filmRow in filmRows:
            self.parseWinnerFilm(filmRow, minNumAwards, afterYear, beforeYear)

    def parseListOfFilms(self, header, minNumAwards, afterYear, beforeYear):
        """Given the the list of films section header, start parsing the list
        header -- The list of films header
        """
        for elem in header.next_siblings:
            if elem.name and elem.name == 'table':
                self.parseFilmTable(elem, minNumAwards, afterYear, beforeYear)

    def getAcademyAwardWinners(self, minNumAwards, afterYear, beforeYear):
        """Get the academy award winners from the Wikipedia list site according to the desired criteria
        minNumAwards -- The minimum number of awards won
        afterYear -- The year after which the film should be made (inclusive)
        beforeYear -- The year before which the film should be made (inclusive)
        """
        f = urllib.request.urlopen(ACADEMY_AWARD_WINNER_LIST_URI)
        soup = BeautifulSoup(f, "html.parser")
        self.films = list()

        for header in soup.find_all(['h2']):
            span = header.span
            if span != None and span['id'] == 'List_of_films':
                self.parseListOfFilms(header, minNumAwards, afterYear, beforeYear)
        return self.films















