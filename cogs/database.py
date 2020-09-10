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
            args = (str(ctx.guild.id), str(ctx.guild.name), str(ch.id), str(ctx.guild.name), str(ch.id))
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            c.execute("SELECT * FROM guilds")
            if column == "starid":         
                c.execute("INSERT INTO guilds (gid, gname, starid) VALUES (?,?,?) ON CONFLICT(gid) DO UPDATE SET gname=?, starid=?",args)
            if column == "roleid":
                c.execute("INSERT INTO guilds (gid, gname, roleid) VALUES (?,?,?) ON CONFLICT(gid) DO UPDATE SET gname=?, roleid=?",args)

            embed = discord.Embed(
                title=f'Successfully bound {channel} to {column}', 
                colour=ctx.author.color
                )
            print(f'{channel} successfully bound to {column} in {ctx.guild.name}')
            conn.commit()
            conn.close
            await ctx.send(embed=embed)    
        @bot.command(
            name='readb',
            description='Reads out all entries in the database row for this guild'
        )
        async def readb(ctx):
            conn = sqlite3.connect('bot.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM guilds WHERE gid=?',(str(ctx.guild.id),))
            r = c.fetchone()
            t = r.keys()
            print(r)
            e = discord.Embed(
                title=f'Database data for {ctx.guild.name}', 
                colour=ctx.author.color
                )
            g = 0
            for item in r: 
                e.add_field(name=f'{t[g]}', value=f'{item}', inline=False)
                g += 1
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(database(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    for guild in bot.guilds:
        gnt = str(guild.name)
        git = str(guild.id)
        c.execute("CREATE TABLE IF NOT EXISTS 'guilds' ('ID' INTEGER,'gid' TEXT UNIQUE,'gname' TEXT,'starid' TEXT,'roleid' TEXT,PRIMARY KEY('ID'))")
    conn.commit()
    conn.close
            
    