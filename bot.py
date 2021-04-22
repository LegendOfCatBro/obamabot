import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from random import choice

#loads the bot token, prefix, and intents
intents = discord.Intents.all()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=commands.when_mentioned_or('obama ', 'hey obama ', ';'), case_insensitive=True, intents=intents) 

#initializing the list of cogs
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
#initializing the cogs when bot is ready
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

#initializing list of possible error titles
bot.error_titles = (
    'fuck', 'shit', "god dammit", "fuck you", 'nope', 'fiddlesticks', 
    'excuse me nigga', 'kill me', 'nice try jackass', 'No way', 
    'the fuck did you just say to me you little shit?', 'i quit',
)
#handling errors   
@bot.event 
async def on_command_error(ctx, error):
    await ctx.message.add_reaction('🖕')
    embed = discord.Embed(
        title=choice(bot.error_titles),
        color=ctx.author.color
    )
    #error for when the command doesnt exist
    if isinstance(error, commands.CommandNotFound):
        embed.description = 'thats not a command'
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.description = f'you are missing an argument'
        embed.add_field(name='command help', value=ctx.command.description)
    elif isinstance(error, commands.TooManyArguments):
        embed.description = 'you provided too many arguments!'
        embed.add_field(name='command help', value=ctx.command.description)
    elif isinstance(error, commands.ArgumentParsingError):
        embed.description = 'unable to parse arguments!'
        embed.add_field(name='commannd help', value=ctx.command.description)    
    elif isinstance(error, commands.BadArgument):
        embed.description = 'you provided a bad argument!'
        embed.add_field(name='command help', value=ctx.command.description)
        
    #errors for bad permissions
    elif isinstance(error, commands.BotMissingPermissions):
        embed.description = (f'i dont have the rights to do that. perms missing: **{error.missing_perms}**')
    elif isinstance(error, commands.MissingPermissions):
        embed.description = (f'you dont have the rights to do that. perms missing: **{error.missing_perms}**')
    elif isinstance(error, commands.ChannelNotReadable):
        embed.description = (f'i dont have the rights to see that channel: **{error.argument.name}**')
    elif isinstance(error, commands.NSFWChannelRequired):
        embed.description = ('that command can only be run in NSFW channels!')
    
    #if an error that isnt handled by the other categories is found
    else:
        embed.description = 'eror!!! report to bot dev'
        embed.add_field(name='unhandled error!!', value=error)
        if ctx.command.description:
            embed.add_field(name='command help', value=ctx.command.description)
    #sends error message
    await ctx.send(embed=embed)
#start the bot 
bot.run(TOKEN)



