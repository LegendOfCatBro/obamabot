import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import find

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(
            name='bind',
            description='Adds the channel ID of the specified channel to the specified column. Essentially, sets the desired channel to serve the desired function.'
        )
        async def bind(ctx, channel: str, column: str):
            print(channel)
            print(column)
            try:
                ch = find(lambda m: m.name == channel, ctx.guild.text_channels)
            except:
                print('Exception on set: Unable to find desired channel!')
                raise commands.BadArgument
            args = (str(ctx.guild.id), str(ctx.guild.name), channel, str(ctx.guild.name), str(ch.id))
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            c.execute("SELECT * FROM guilds")
            if column == "starid":         
                c.execute("INSERT INTO guilds (gid, gname, starid) VALUES (?,?,?) ON CONFLICT(gid) DO UPDATE SET gname=?, starid=?",args)
            if column == "roleid":
                c.execute("INSERT INTO guilds (gid, gname, roleid) VALUES (?,?,?) ON CONFLICT(gid) DO UPDATE SET gname=?, roleid=?",args)
            else:
                print('Exception on set: Unable to find desired function')
                raise commands.BadArgument
            embed = discord.Embed(
                title=f'Successfully bound {channel} to {column}', 
                colour=ctx.author.color
                )
            print(f'{channel} successfully bound to {column} in {ctx.guild.name}')
            await ctx.send(embed=embed)    



def setup(bot):
    bot.add_cog(database(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
       
    starboard_name = 'starboard'
    for guild in bot.guilds:
        gnt = str(guild.name)
        git = str(guild.id)
        c.execute("CREATE TABLE IF NOT EXISTS 'guilds' ('ID' INTEGER,'gid' TEXT UNIQUE,'gname' TEXT,'starid' TEXT,'roleid' TEXT,PRIMARY KEY('ID'))")
    for row in c.execute('SELECT * FROM guilds ORDER BY ID'):
        print(row)
    conn.commit()
    conn.close
            
    