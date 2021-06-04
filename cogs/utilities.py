import os
import discord
from discord.ext import commands

class utilities(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='reload', 
        decription='**obama reload {cog}**: reloads specified cog'
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
        await ctx.message.add_reaction('👍')

    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='unload',
        description='**obama unload {cog}**: unloads specified cog'
    )
    async def unload(self, ctx, ext):
        cog = f"cogs.{ext}"
        self.bot.unload_extension(cog)
        print(f'Successfully unloaded {cog}')
        await ctx.message.add_reaction('👍')
    
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())    
    @commands.command(
        name='load', 
        description='**obama load {cog}**: loads specified cog'
    )
    async def load(self, ctx, ext):
        cog = f"cogs.{ext}"
        self.bot.load_extension(cog)
        print(f'Successfully loaded {cog}')
        await ctx.message.add_reaction('👍')
def setup(bot):
    bot.add_cog(utilities(bot))   