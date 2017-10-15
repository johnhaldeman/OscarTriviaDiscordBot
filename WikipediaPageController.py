import urllib.request
from bs4 import BeautifulSoup

ACADEMY_AWARD_WINNER_LIST_URI = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

class Film(object):
    """Data Object for a Film"""

    def __init__(self, numAwards, year, uri):
        """numAwards -- The number of academy awards recieved
        year -- The year the film was made
        uri -- the uri of the Wikipedia entry for the film"""
        self.numAwards = numAwards
        self.year = year
        self.uri = uri


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

    def getAcademyAwardWinners(self, numAwards, afterYear):
        f = urllib.request.urlopen(ACADEMY_AWARD_WINNER_LIST_URI)
        soup = BeautifulSoup(f, "html.parser")

        for header in soup.find_all(['h2']):
            span = header.span
            if span != None and span['id'] == 'List_of_films':
                for elem in header.next_siblings:
                    if elem.name and elem.name == 'table':
                        print(elem)











