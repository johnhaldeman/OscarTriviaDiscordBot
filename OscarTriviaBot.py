
from WikipediaPageController import WikipediaPageController

pageController = WikipediaPageController()


films = pageController.getAcademyAwardWinners(0, 0, 9999)

for film in films:
    print(film)
    print()


