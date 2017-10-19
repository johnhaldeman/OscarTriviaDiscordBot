from WikipediaPageController import WikipediaPageController
from random import randrange
from random import shuffle
from random import sample


pageController = WikipediaPageController()

films = pageController.getAcademyAwardWinners(5, 1980, 3000)
index = randrange(0, len(films), 1)
film = films[index]

keywords =  pageController.parseOutKeywords("https://en.wikipedia.org" + film.uri)

guessed = False

print("Let's play password!")
print("I've picked an oscar winner from Wikipedia and will give you 1 word (ish) clues. Try to guess in 10 clues or less\n\n")

for i in range(10):
    keyword = sample(keywords, 1)[0]
    answer = input(keyword + ": ")
    if(answer.upper() == film.title.upper()):
        guessed = True
        break
    else:
        print("Nope! here's another clue.\n")
    keywords.remove(keyword)

if guessed:
    print ("Good Job!")
else:
    print ("Better Luck Next Time! The answer was: " + film.title)
