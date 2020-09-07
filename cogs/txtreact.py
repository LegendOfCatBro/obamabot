import os
import discord
from discord.ext import commands

class txtreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        if message.author == self.bot.user:
            return
        elif msg == 'fuck':
            reply = "me ( ͡° ͜ʖ ͡°)"
            await message.channel.send(reply)
            print("Reaction triggered: fuck")
        elif "uwu" in msg:
            reply = """ᵘʷᵘ   oh frick ᵘʷᵘ ᵘʷᵘ
ᵘʷᵘ      ᵘʷᵘ           ᵘʷᵘ 
   ᵘʷᵘ
         ᵘʷᵘ      ᵘʷᵘ     frick sorry guys
ᵘʷᵘ             ᵘʷᵘ ᵘʷᵘ     ᵘʷᵘ
ᵘʷᵘ  ᵘʷᵘ sorry im dropping 
ᵘʷᵘ my uwus all over the ᵘʷᵘ place  ᵘʷᵘ
   ᵘʷᵘ     ᵘʷᵘ sorry"""
            await message.channel.send(reply)
            print("Reaction triggered: uwu")

def setup(bot):
    bot.add_cog(txtreact(bot))