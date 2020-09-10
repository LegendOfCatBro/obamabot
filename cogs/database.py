import os
import discord
import sqlite3
import json
from discord.ext import commands
from discord.utils import find

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.command(
            name='eunbind',
            desciption='Removes the emoji and role pair from the self-assign role database'
        )
        async def ebind(ctx, emo:str, role:str):
            gid = str(ctx.guild.id)
            rgid = f"{gid}{emo}"
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            try:
                c.execute("DELETE FROM roles WHERE rgid=?",(rgid,))
            except:
                print('Exception on eunbind: Unable to find desired row!')
                x = discord.Embed(title='Error!', description='Error deleting desired row!', color =0x7C0A02) 
                await ctx.send(embed = x)
            conn.commit()
            conn.close
            embed = discord.Embed(
                title=f'Successfully unbound {emo} from {role}', 
                colour=ctx.author.color
                )
            await ctx.send(embed = embed)
        @bot.command(
            name='ebind',
            description='Adds the emoji and role pair to the self-assign role database'
        )
        async def ebind(ctx, emo: str, role: str):
            try:
                r = find(lambda m: m.name == role, ctx.guild.roles)
            except:
                print('Exception on ebind: Unable to find desired role!')
                x = discord.Embed(title='Error!', description='Error finding desired role!', color =0x7C0A02) 
                await ctx.send(embed = x)
            gid = str(ctx.guild.id)
            rid = str(r.id)
            rgid = f"{gid}{emo}"
            args = (gid, emo, rid, rgid, gid, emo, rid) 
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            c.execute("SELECT * FROM roles")
            c.execute("INSERT INTO roles (gid,emo,rid,rgid) VALUES (?,?,?,?) ON CONFLICT(rgid) DO UPDATE SET gid=?,emo=?,rid=?",args)
            conn.commit()
            conn.close
            embed = discord.Embed(
                title=f'Successfully bound {emo} to {role}', 
                colour=ctx.author.color
                )
            await ctx.send(embed=embed) 
        @bot.command(
            name='bind',
            description='Adds the channel ID of the specified channel to the specified column. Essentially, sets the desired channel to serve the desired function.'
        )
        async def bind(ctx, channel: str, column: str):
            try:
                ch = find(lambda m: m.name == channel, ctx.guild.text_channels)
            except:
                print('Exception on bind: Unable to find desired channel!')
                x = discord.Embed(title='Error!', description='Error finding desired channel!', color =0x7C0A02) 
                await ctx.send(embed = x)
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
        async def readb(ctx, table: str):
            conn = sqlite3.connect('bot.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if table == 'guilds':
                c.execute('SELECT * FROM guilds WHERE gid=?',(str(ctx.guild.id),))
            if table == 'roles':
                c.execute('SELECT * FROM roles WHERE gid=?',(str(ctx.guild.id),))
            e = discord.Embed(
                title=f'Database data for {ctx.guild.name}', 
                colour=ctx.author.color
                )
            for row in c.fetchall():
                t = row.keys()
                g = 0
                for item in row:
                    e.add_field(name=f'{t[g]}', value=f'{item}', inline=False)
                    g += 1
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(database(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'guilds' ('id' INTEGER,'gid' TEXT UNIQUE,'gname' TEXT,'starid' TEXT,'roleid' TEXT,PRIMARY KEY('id'))")
    c.execute("CREATE TABLE IF NOT EXISTS 'roles' ('id' INTEGER,'gid' TEXT,'emo' TEXT,'rid' TEXT,'rgid' TEXT UNIQUE,PRIMARY KEY('id'))")
    conn.commit()
    conn.close
            
    