import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import find
from random import choice

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='opunbind',
        desciption='**obama opunbind {table} {row}**: Operator unbind, removes an item from the given table. Valid tables include: **ugconfig**, **gconfig**, and **userroles**.'
    )
    async def opunbind(self, ctx, tbl, row):
        tblnames=('guconfig','gconfig','userroles')
        if not row.isnumeric() or tbl not in tblnames:
            raise commands.BadArgument()
            return
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        arg = (row, ctx.guild.id)
        c.execute(f"DELETE FROM {tbl} WHERE rowid=? AND id=?", arg)
        conn.commit()
        conn.close

        await ctx.message.add_reaction('👍')
    
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='config',
        description='`obama config {job} {value} {valuetype}`: Binds a new item to the config table. Try `obama confighelp` for details on valid jobs and value type combinations.'
    )
    async def config(self, ctx, job, inpvalue, valuetype):
        value=inpvalue
        job = job.upper()
        valuetype=valuetype.upper()
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        validtypes=('ROLE', 'CHANNEL', 'MESSAGE', 'STRING')
        if valuetype not in validtypes:
            raise commands.BadArgument()
            return
        validtypes={'ROLE':ctx.guild.roles,'CHANNEL':ctx.guild.channels} 
        if valuetype == "ROLE" or valuetype == "CHANNEL":
            value = find(lambda m: m.name == value, validtypes[valuetype]).id
        elif valuetype == "MESSAGE":
            value = value.split('/')[6]
        id=ctx.guild.id
        args = (id,job,str(value),valuetype)
        uniquejobs=('STARCHANNEL','ROLECHANNEL','STARTHRESHOLD','STAREMOJI')
        if job in uniquejobs:
            args = args + (str(id)+job, id, job, str(value), valuetype)
            c.execute("INSERT INTO guconfig (id, job, value, valuetype, uniqueid) VALUES (?,?,?,?,?) ON CONFLICT(uniqueid) DO UPDATE SET id=?, job=?, value=?, valuetype=?", args)
            print(f"unique config changed: {job} {value} {valuetype}")
        else:
            c.execute("INSERT INTO gconfig (id, job, value, valuetype) VALUES (?,?,?,?)", args)
            print(f"config added: {job} {value} {valuetype}")
        await ctx.message.add_reaction('👍')
        conn.commit()
        conn.close    


    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='readb',
        description='**obama readb {table}**: Reads out all entries related to the current guild in the given database table'
    )
    async def readb(self, ctx, table):
        conn = sqlite3.connect('bot.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        e = discord.Embed(
            title=f'Database data for {ctx.guild.name}', 
            colour=ctx.author.color
            )
        tablenames=('guconfig','gconfig','userroles', 'users', 'punish')
        if table not in tablenames:
            raise commands.BadArgument()
        id = ctx.guild.id
        c.execute(f'SELECT rowid, * FROM {table} WHERE id = {ctx.guild.id}')
        dd=c.fetchall()
        fields = 0
        pages = 1
        
        for row in dd:
            t = row.keys()
            itms = 0
            rw = f''
            for item in row:
                rw += f'[{t[itms]}: {item}]'
                itms += 1
            if fields == 24:
                e.add_field(name='Error!', value='Too many rows, going to next page')
                pages += 1
                fields = 0
                await ctx.send(embed=e)
                e = discord.Embed(
                    title=f'Database data for {ctx.guild.name} part {pages}', 
                    colour=ctx.author.color
                    )
            else:    
                e.add_field(name=f"row {row['rowid']}: ", value=rw)
                fields += 1
        if fields == 0:
            e.add_field(name='Error!', value='Table is empty')
        await ctx.send(embed=e)
        await ctx.message.add_reaction('👍')
    
def setup(bot):
    bot.add_cog(database(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'guconfig' ('id' INT, 'job' TEXT,'value' TEXT, 'valuetype' TEXT, 'uniqueid' TEXT UNIQUE)")
    c.execute("CREATE TABLE IF NOT EXISTS 'gconfig' ('id' INT, 'job' TEXT, 'value' TEXT, 'valuetype' TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS 'userroles' ('id' INT, 'uid' INT, 'rid' INT, 'rname' TEXT,'color' TEXT, 'uniqueid' TEXT UNIQUE)")
    c.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INT UNIQUE, 'name' TEXT, 'birthday' TEXT, 'location' TEXT, 'timezone' TEXT, 'pronouns' TEXT, 'sexuality' TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS 'punish' ('id' INT, 'uid' INT, 'punishment' TEXT, 'start' TEXT,'end' TEXT, 'uniqueid' TEXT UNIQUE)")
    conn.commit()
    conn.close
            
    