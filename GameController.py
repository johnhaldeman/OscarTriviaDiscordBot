from WikipediaPageController import WikipediaPageController
from WikipediaPageController import Film
from random import randrange
from random import shuffle
from random import sample
import copy

MAX_GUESSES = 10
WIKIPEDIA_BASE_URI = "https://en.wikipedia.org"
MIN_AWARDS = 5
MIN_YEAR = 1960
MAX_YEAR = 3000
HELP_TEXT = '''I am a oscarbot!
You can play a password-like game with me.

This is how it works:
1) I pick an oscar winning film
2) I give you clues that are key words or phrases from the film's Wikipedia article
3) You guess the film's name based on those clues
I keep giving you clues and you keep guessing. If you get the answer in under 10 guesses, you win!

To start playing, type %start
'''

class Game(object):
    """Represents an individual's game and the state of it"""

    GS_NONE = 0;
    GS_START = 1;
    GS_GUESSING = 2;
    GS_SUCCESS = 3;
    GS_FAILED = 4;

    def __init__(self, user, films):
        self.user = user
        self.numGuesses = 0
        self.state = Game.GS_NONE        
        self.films = copy.deepcopy(films)
        self.currentFilm = None

    def computeState(self, comm):
        if comm == '%start' and self.state != Game.GS_GUESSING:
            self.initGame()        
            self.state = Game.GS_START
        elif self.state == Game.GS_GUESSING or self.state == Game.GS_START:
            if self.currentFilm.title.lower().strip() == comm.lower().strip():
                self.state = Game.GS_SUCCESS
                self.numGuesses = 0
            elif self.numGuesses < MAX_GUESSES + 1:
                self.numGuesses = self.numGuesses + 1
                self.state = Game.GS_GUESSING
            else:
                self.state = Game.GS_FAILED
                self.numGuesses = 0

    def initGame(self):
        index = randrange(0, len(self.films), 1)
        self.currentFilm = self.films[index]
        del(self.films[index])
        self.keywordSetList =  self.currentFilm.keywordSetList

    def nextClue(self):
        if len(self.keywordSetList[0]) > 0:
            keywordSet = self.keywordSetList[0]
        else:
            keywordSet = self.keywordSetList[1]
        
        keyword = sample(keywordSet, 1)[0]
        keywordSet.remove(keyword)

        return keyword


class GameController(object):
    """Maintains a registry of games and controls game state"""

    def __init__(self, films):
        self.games = dict()
        self.films = films

    def processCommand(self, command, user):
        comm = command.lower()
        if user in self.games:
            currGame = self.games[user]
        else:
            currGame = Game(user, self.films)
            self.games[user] = currGame
        if comm == '%help':
            return HELP_TEXT

        currGame.computeState(command)

        if currGame.state == Game.GS_NONE:
            return "To learn about how to play with oscarbot, type %help"
        elif currGame.state == Game.GS_START:
            return "Let's start a new game! Your first clue is:\n" + currGame.nextClue()
        elif currGame.state == Game.GS_GUESSING:
            return "Nope, that's not it. Your next clue is:\n" + currGame.nextClue()
        elif currGame.state == Game.GS_SUCCESS:
            return "Great Job!!! You guessed right! The answer was:\n" \
                + self.getAnswer(currGame) + ".\n" \
                + "Type %start to start a new game"
        elif currGame.state == Game.GS_FAILED:
            return "You've had ten guesses but failed to guess the film. The answer was:\n" \
                + self.getAnswer(currGame) + ".\n" \
                + "Type %start to start a new game"

    def getAnswer(self, game):
        return game.currentFilm.title + "\n" + WIKIPEDIA_BASE_URI + game.currentFilm.uri





