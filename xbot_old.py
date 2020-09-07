import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
#simple reactions
    if message.author == client.user:
        return
    if message.content.lower() == "ping":
       reply = "pong"
       await message.channel.send(reply)
       print("Message sent: " + reply)
    if "obama" in message.content.lower():
       reply = "oi"
       await message.channel.send(reply)
#image reactions
       print("Message sent: " + reply)   
    if message.content.lower() == "shut up":
       reply = "https://preview.redd.it/vmb3thssj4921.png?auto=webp&s=3a3e737c3957950543eeea2e38d71496e6d8bc9d"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(silence liberal.jpeg)")
    if message.content.lower() == "whomst has summoned the almighty one":
       reply = "https://i.imgflip.com/3ia3r2.png"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(whomst has summoned the almighty one.png)")
    if message.content.lower() == "arrivederci":
       reply = "https://i.ytimg.com/vi/WKGs20VchQs/maxresdefault.jpg"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(arrivederci.jpg)")   
    if "uwu" in message.content.lower():
       reply = """ᵘʷᵘ   oh frick ᵘʷᵘ ᵘʷᵘ
ᵘʷᵘ      ᵘʷᵘ           ᵘʷᵘ 
   ᵘʷᵘ
         ᵘʷᵘ      ᵘʷᵘ     frick sorry guys
ᵘʷᵘ             ᵘʷᵘ ᵘʷᵘ     ᵘʷᵘ
ᵘʷᵘ  ᵘʷᵘ sorry im dropping 
ᵘʷᵘ my uwus all over the ᵘʷᵘ place  ᵘʷᵘ
   ᵘʷᵘ     ᵘʷᵘ sorry
       """
       await message.channel.send(reply)
       print("Message sent: " + reply)     
    if message.content.lower() == "fuck":
       reply = "me ( ͡° ͜ʖ ͡°)"
       await message.channel.send(reply)
       print("Message sent: " + reply)
    if message.content.lower() == "i refuse":
       reply = "https://i.ytimg.com/vi/QQ80PbfYwtU/maxresdefault.jpg"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(i refuse.jpg)")    
    if message.content.lower() == "smol brian" or message.content.lower() == "smol brain":
       reply = "https://i.imgflip.com/3ho6l0.jpg"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(smol brain.jpg)") 
    if message.content.lower() == "go to horny jail":
       reply = "https://cdn.discordapp.com/attachments/632409348647157772/696178608624107642/image0.png"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(go to horny jail.png)")     
    if message.content.lower() == "nice":
       reply = "https://cdn.discordapp.com/attachments/632409348647157772/692797839587278859/dd4zo17-4232348f-4b0a-4356-87e3-608d6b2ff06d.png"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(nice.png)")
    if message.content.lower() == "shut":
       reply = "https://i.imgflip.com/3g5hqc.png"
       await message.channel.send(reply)
       print("Message sent: " + reply + "(shut.png)")       
client.run(TOKEN)
