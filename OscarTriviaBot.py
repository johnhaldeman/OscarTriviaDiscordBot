import discord
import asyncio
import sys
from FilmFileHandler import FilmFileHandler
from GameController import GameController

fh = FilmFileHandler()

if(sys.argv[1] == 'run'):
    client = discord.Client()
    films = fh.readSerializedFilms()
    gc = GameController(films)

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        print("-------------------")
        print(message.author.name)
        if(message.channel.is_private):
            print("in private channel")
        else:
            print("in " + message.channel.server.name + ":" + message.channel.name)
        print("-------------------")
        print(message.content)
        if message.author.name == 'oscarbot':
            return
        elif message.channel.is_private:
             await client.send_message(message.channel, gc.processCommand(message.content, message.author.id))
        else:
           for member in message.mentions:
               if member.name == 'oscarbot':
                   await client.send_message(message.channel, "Thanks for mentioning me! If you'd like to play a game, send me a private message (PM)")
                   break
            
    client.run(sys.argv[2])

else:
    fh.writeSerializedFilms(4, 1960, 3000)


