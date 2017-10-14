from bs4 import BeautifulSoup
import urllib.request

f = urllib.request.urlopen("https://en.wikipedia.org/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)")
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

for keyword in keywords:
    print(keyword)
