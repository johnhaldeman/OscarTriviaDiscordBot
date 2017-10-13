from bs4 import BeautifulSoup
import urllib.request

f = urllib.request.urlopen("https://en.wikipedia.org/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)")
soup = BeautifulSoup(f, "html.parser")

for header in soup.find_all(['h2']):
    span = header.span
    if span != None and span['id'] in ('Plot', 'Cast'):
        print(span['id'])
        for elem in header.next_siblings:
            if elem.name and elem.name.startswith('h'):
                break;
            if elem.name == 'p':
                print(elem.get_text())

