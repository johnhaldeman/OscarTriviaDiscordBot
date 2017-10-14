from bs4 import BeautifulSoup
from WikipediaPageController import WikipediaPageController

pageController = WikipediaPageController()

keywords = pageController.parseOutKeywords("https://en.wikipedia.org/wiki/Fantastic_Beasts_and_Where_to_Find_Them_(film)")

for keyword in keywords:
    print(keyword)

