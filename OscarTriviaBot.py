import discord
import asyncio
import sys
from GameController import GameController

client = discord.Client()
gc = GameController();

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


client.run(sys.argv[1])

