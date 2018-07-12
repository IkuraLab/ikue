import discord
import asyncio
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith("!hi"):
        if client.user != message.author:
            m = "hi!" + message.author.name + "!"
            await client.send_message(message.channel, m)

client.run("")