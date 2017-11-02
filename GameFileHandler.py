
import os.path

DIR_PATH = "games/"

class GameFileHandler(object):

    def getFileName(self, userID):
        return DIR_PATH + userID + ".json"
    
    def writeSerializedGame(self, userID, gameData):
        with open(self.getFileName(userID), 'w') as f:
            f.write(gameData)


    def readSerializedGame(self, userID):
        with open(self.getFileName(userID), 'r') as f:
            gamein = f.read()
            return gamein

        
    def isSavedGame(self, userID):
        return os.path.isfile(self.getFileName(userID))



