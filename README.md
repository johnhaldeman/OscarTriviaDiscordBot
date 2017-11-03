# OscarTriviaDiscordBot
Play the game "Password" with a Discord bot focusing on Oscar trivia.

# How the bot works
The bot downloads and parses the Wikipedia page containing all Academy Award winning films. It then returns a list of films based on criteria provided such as the minimum number of awards won and the years the films were awarded in. Once the list of films is retrieved it then parses each film's Wikipedia entry and returns a list of keywords and phrases in the Plot and Cast sections. The keywords are chosen based on whether the word is a link or not. Because the HTML parsing takes some time, the parsing is done once and then subsequently fed to the bot on startup.

# Play a Game with the Bot
In order to play a game with the bot you need to be able to private message it. To private message with the bot, you need to be part of a Discord server that has the bot added. If you'd like to play you can join this server:

https://discord.gg/9qQDsdJ


# Screenshots
<img alt="Answering a question successfully after many guesses" src="https://github.com/johnhaldeman/OscarTriviaDiscordBot/blob/master/screenshots/AnsweringSucessfully.png" height="600px">

<img alt="Answering a question wrong and then getting the next one quickly" src="https://github.com/johnhaldeman/OscarTriviaDiscordBot/blob/master/screenshots/MixOfAnswers.png" height="600px">

# How to start your own bot
First execute OscarTriviaBot.py with no command line arguments. This will create or refresh the films.json file that contains the required information from Wikipedia.

Once films.json is created, run OscarTriviaBot.py providing it the command line options "run" along with the bot's discord client secret. For example:
```
python OscarTriviaBot.py run AAABBBCCCCDDD
```
replacing `AAABBBCCCCDDD` with your bot's client secret

# Dependancies
1. Python 3.6
2. [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
3. [discord.py](https://github.com/Rapptz/discord.py)

