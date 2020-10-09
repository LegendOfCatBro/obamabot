import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from random import choice

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=('obama ', 'hey obama '))
bot.error_titles = (
    'fuck', 'shit', "god dammit", "fuck you", 'nope', 'fiddlesticks', 
    'excuse me nigga', 'kill me', 'nice try jackass', 'No way', 
    'the fuck did you just say to me you little shit?', 'i quit',
)  

cogs = []

for (dirpath, dirnames, filenames) in os.walk(f'{os.getcwd()}/cogs/'):
    if '__pycache__' not in dirpath:
        cogs += [
            os.path.join(dirpath, file).replace(
               f'{os.getcwd()}/', 
                ''
            ).replace('.py', '').replace('/', '.') 
            for file in filenames
        ]
print(f'Connecting to discord...')
@bot.event
async def on_ready():
    print(f'Loading cogs...')
    if not bot.cogs:
        for cog in cogs:
            try:
                if cog not in bot.cogs.values() and 'pycache' not in cog:
                    bot.load_extension(cog)
                    print(f'Successfully loaded {cog}')
            except Exception as e:
                print(f'Error on loading {cog}:\n{e}')
    print(f'Successfully connected to discord!')
@bot.event 
async def on_command_error(ctx, error):
    await ctx.message.add_reaction('🖕')
    embed = discord.Embed(
        title=choice(bot.error_titles),
        color=ctx.author.color
    )
    if isinstance(error, commands.CommandNotFound):
        embed.description = 'thats not a command'
    elif isinstance(error, asyncio.TimeoutError):
        embed.description = 'too slow'
    elif isinstance(error, commands.MissingPermissions):
        embed.description = (
            'you dont have the rights 😤'
            f'command: **{error.missing_perms[0]}**.'
        )
    elif isinstance(error, commands.BadArgument):
        embed.description = 'Bad Argument!'
        if ctx.command.description:
            embed.add_field(
                name='command help', 
                value=ctx.command.description
            )
    else:
        embed.description = 'eror !!!'
        embed.add_field(
            name='error', 
            value=error
        )
        if ctx.command.description:
            embed.add_field(
                name='command help', 
                value=ctx.command.description
            )
    await ctx.send(embed=embed)
    
    
@bot.command(description=f'reloads the specified cog')
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def reload(ctx, *, ext):
    cog = f"cogs.{ext}"
    try:
        bot.unload_extension(cog)
        print(f'Successfully unloaded {cog}')
    except commands.ExtensionNotLoaded:
        pass
    bot.load_extension(cog)
    print(f'Successfully loaded {cog}')
    embed = discord.Embed(
            title='reload successful', 
            description=(f'Successfully reloaded {cog}'), 
            colour=ctx.author.color
            )
    await ctx.send(embed=embed)

@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
@bot.command(description=f'unloads the specified cog')
async def unload(ctx, *, ext):
    cog = f"cogs.{ext}"
    bot.unload_extension(cog)
    print(f'Successfully unloaded {cog}')
    embed = discord.Embed(
            title='unload successful', 
            description=(f'Successfully unloaded {cog}'), 
            colour=ctx.author.color
            )
    await ctx.send(embed=embed)

@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())    
@bot.command(description=f'loads the specified cog')
async def load(ctx, *, ext):
    cog = f"cogs.{ext}"
    bot.load_extension(cog)
    print(f'Successfully loaded {cog}')
    embed = discord.Embed(
            title='load successful', 
            description=(f'Successfully loaded {cog}'), 
            colour=ctx.author.color
            )
    await ctx.send(embed=embed)
    
bot.run(TOKEN)

