import os
import discord
import hashlib
from discord.ext import commands
from hashlib import blake2b

class NAME(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='',
        description=''
    )
    async def NAME(self, ctx):
        embed = discord.Embed(
            title='', 
            description='', 
            colour=ctx.author.color
            )
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(NAME(bot))
    
    #hash thingy: 
hash = blake2b(digest_size=1, key=b'wombat')
hash.update(b'fuck')
print(round(int(hash.hexdigest(), 16)/2.56))