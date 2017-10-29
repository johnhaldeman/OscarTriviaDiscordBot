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
        print(message.content)
        if not message.author.name == 'oscarbot':
            await client.send_message(message.channel, gc.processCommand(message.content, message.author.id))
            
    client.run(sys.argv[2])

else:
    fh.writeSerializedFilms(4, 1960, 3000)


