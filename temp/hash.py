#all the commands that use the hash function to turn a string into numbers
import os
import discord
import hashlib
from discord.ext import commands
from hashlib import blake2b

class hashbrowns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    
def setup(bot):
    bot.add_cog(hashbrowns(bot))