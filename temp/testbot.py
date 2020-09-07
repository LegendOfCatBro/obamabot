import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content == 'test':
        embed = discord.Embed(
            title='Test', 
            description='Test', 
            )
        await message.channel.send(embed=embed)
    

client.run(TOKEN)