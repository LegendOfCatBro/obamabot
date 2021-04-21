import os
import discord
from discord.ext import commands

class utilities(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='reload', 
        decription='reloads the specified cog'
    )
    async def reload(self, ctx, ext):
        cog = f"cogs.{ext}"
        try:
            self.bot.unload_extension(cog)
            print(f'Successfully unloaded {cog}')
        except commands.ExtensionNotLoaded:
            pass
        self.bot.load_extension(cog)
        print(f'Successfully loaded {cog}')
        embed = discord.Embed(
                title='reload successful', 
                description=(f'Successfully reloaded {cog}'), 
                colour=ctx.author.color
                )
        await ctx.send(embed=embed)

    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='unload',
        description='unloads the specified cog'
    )
    async def unload(self, ctx, ext):
        cog = f"cogs.{ext}"
        self.bot.unload_extension(cog)
        print(f'Successfully unloaded {cog}')
        embed = discord.Embed(
                title='unload successful', 
                description=(f'Successfully unloaded {cog}'), 
                colour=ctx.author.color
                )
        await ctx.send(embed=embed)
    
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())    
    @commands.command(
        name='load', 
        description='loads the specified cog'
    )
    async def load(self, ctx, ext):
        cog = f"cogs.{ext}"
        self.bot.load_extension(cog)
        print(f'Successfully loaded {cog}')
        embed = discord.Embed(
                title='load successful', 
                description=(f'Successfully loaded {cog}'), 
                colour=ctx.author.color
                )
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(utilities(bot))   