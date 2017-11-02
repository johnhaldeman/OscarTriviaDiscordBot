from WikipediaPageController import WikipediaPageController
from WikipediaPageController import Film
from GameFileHandler import GameFileHandler
from random import randrange
from random import shuffle
from random import sample
import copy
import json
import collections

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

You might be wondering how I pick the movies and get the clues. Well, I get that information automatically from Wikipedia. Sometimes I make good choices, sometimes I don't. Hopefully I make mostly good ones.

To start playing, type %start
'''

class Game(object):
    """Represents an individual's game and the state of it"""

    GS_NONE = 0;
    GS_START = 1;
    GS_GUESSING = 2;
    GS_SUCCESS = 3;
    GS_FAILED = 4;
    GS_END = 5;

    def __init__(self, user, films):
        self.user = user
        self.numGuesses = 0
        self.state = Game.GS_NONE        
        self.films = copy.deepcopy(films)
        self.guessedRight = 0
        self.totalQuestions = 0
        self.currentFilm = None

    def computeState(self, comm):
        if len(self.films) == 0:
            self.state = Game.GS_END
        elif comm == '%start' and self.state != Game.GS_GUESSING:
            self.initGame()        
            self.state = Game.GS_START
            self.totalQuestions = self.totalQuestions + 1
        elif self.state == Game.GS_GUESSING or self.state == Game.GS_START:
            if self.currentFilm.title.lower().strip() == comm.lower().strip():
                self.state = Game.GS_SUCCESS
                self.numGuesses = 0
                self.guessedRight = self.guessedRight + 1
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
        self.fileHandler = GameFileHandler()

    def serializeGame(self, game):
        def defaultHandler(obj):
            if isinstance(obj, collections.Set):
                return list(obj)
            else:
                return obj.__dict__
        return json.dumps(game, default=defaultHandler)

    def deserializeGame(self, gameData):
        def asGame(gameDict):
            if 'title' in gameDict:
                return Film(gameDict['title'], gameDict['year'], gameDict['numAwards'], gameDict['numNominations'], gameDict['uri'], keywordSetList=gameDict['keywordSetList'])
            elif 'user' in gameDict:
                game = Game(gameDict['user'], gameDict['films'])
                game.numGuesses = gameDict['numGuesses']
                game.state = gameDict['state']
                game.currentFilm = gameDict['currentFilm']
                game.keywordSetList = gameDict['keywordSetList']
                game.guessedRight = gameDict['guessedRight']
                return game
            else:
                print("Can't deserialize object: " + gameData)
                return None

        game = json.loads(gameData, object_hook = asGame)
        for film in game.films:
            # Weird thing - Deserialization created a whole new game. We just want it to point to the game in the current list
            if film.title == game.currentFilm.title:
                game.currentFilm = film
                game.keywordSetList = film.keywordSetList

        return game


    def processCommand(self, command, user):
        comm = command.lower()
        if user in self.games:
            currGame = self.games[user]
        elif self.fileHandler.isSavedGame(user):
            gameData = self.fileHandler.readSerializedGame(user)
            currGame = self.deserializeGame(gameData)
            self.games[user] = currGame
        else:
            currGame = Game(user, self.films)
            self.games[user] = currGame
        if comm == '%help':
            return HELP_TEXT

        currGame.computeState(command)

        if(currGame.state != Game.GS_NONE):
            self.fileHandler.writeSerializedGame(user, self.serializeGame(currGame))
        
        if currGame.state == Game.GS_NONE:
            return "To learn about how to play with oscarbot, type %help"
        elif currGame.state == Game.GS_START:
            return "Let's start a new game! So far you have guessed " \
                + str(currGame.guessedRight) + "/" + str(currGame.totalQuestions) + " films correctly. " \
                + "Your first clue for the next film is:\n" + str(currGame.nextClue())
        elif currGame.state == Game.GS_GUESSING:
            return "Nope, that's not it. Your next clue is:\n" + currGame.nextClue()
        elif currGame.state == Game.GS_SUCCESS:
            return "Great Job!!! You guessed right! The answer was:\n" \
                + self.getAnswer(currGame) + ".\n" \
                + "Type %start to start a new game"
        elif currGame.state == Game.GS_FAILED:
            return "You've had ten guesses but failed to guess the film. The answer was:\n" \
                + self.getAnswer(currGame) + ".\n" \
                + "Type %start to start a new game. There are " + len(currGame.films) + " films left"
        elif currGame.state == Game.GS_END:
            return "That's all there is! You've attempted to guess all the films!"
        


    def getAnswer(self, game):
        return game.currentFilm.title + "\n" + WIKIPEDIA_BASE_URI + game.currentFilm.uri





