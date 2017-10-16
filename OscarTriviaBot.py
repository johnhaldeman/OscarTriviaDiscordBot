
from WikipediaPageController import WikipediaPageController

pageController = WikipediaPageController()


films = pageController.getAcademyAwardWinners(0, 0)

for film in films:
    print(film)
    print()


