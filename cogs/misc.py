import discord
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping',
        description='pong!'
    )
    async def ping(self, ctx):
        desc = f'latency: {self.bot.latency:.5f}s'
        embed = discord.Embed(
            title='pong !!!!', 
            description=desc, 
            colour=ctx.author.color
            )
        print(f'Command invoked: Ping')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(misc(bot))