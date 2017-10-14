import urllib.request
from bs4 import BeautifulSoup

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

        keywords = [];

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
                                keywords.append(text)
        return keywords






