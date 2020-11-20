import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import find

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='utilunbind',
        desciption='Binds an item to a slot in the database'
    )
    async def utilunbind(self, ctx, tbl, row):
        if not row.isnumeric():
            print('Exception on unbind: Row ID must be a numeral!')
            x = discord.Embed(title='Error!', description='Row ID must be a numeral!', color =0x7C0A02) 
            await ctx.send(embed = x)
            return
        if tbl == 'guilds':
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            arg = (row, str(ctx.guild.id))
            c.execute("DELETE FROM guilds WHERE rowid=? AND id=?", arg)
            conn.commit()
            conn.close
        x = discord.Embed(title='unbinding successful',description=f'item {row} successfully unbound',color=ctx.author.color) 
        await ctx.send(embed = x)
    
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='utilbind',
        desciption='Binds an item to a slot in the database'
    )
    async def uitilbind(self, ctx, inp1, inp2):
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        if inp2.isalpha():
            t = ctx.guild.text_channels
        else:
            t = ctx.guild.roles
        inp3 = find(lambda m: m.name == inp1, t)
        if not inp1:
            print('Exception on bind: Unable to find desired objecct!')
            x = discord.Embed(title='Error!', description='Error finding desired object!', color =0x7C0A02) 
            await ctx.send(embed = x)
            return
        imp1 = str(inp3.id)
        id = str(ctx.guild.id)
        gid = str(ctx.guild.id) + inp2
        arg = (id, imp1, inp2, gid, id, imp1, inp2)
        if inp2.isalpha():
            arg = (id, inp2, imp1, gid, id, inp2, imp1)
            print(arg)
        c.execute("INSERT INTO guilds (id, role, emoch, rgid) VALUES (?,?,?,?) ON CONFLICT(rgid) DO UPDATE SET id=?, role=?, emoch=?", arg)
        print("bind2 successful")
        x = discord.Embed(title='binding successful',description=f'{inp1} bound to {inp2}',color=ctx.author.color) 
        await ctx.send(embed = x)
        conn.commit()
        conn.close    
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    @commands.command(
        name='readb',
        description='Reads out all entries in the database row for this guild'
    )
    async def readb(self, ctx, table):
        conn = sqlite3.connect('bot.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        e = discord.Embed(
            title=f'Database data for {ctx.guild.name}', 
            colour=ctx.author.color
            )
        if table == 'guilds':
            gg = (str(ctx.guild.id),)
            c.execute('SELECT rowid, id, role, emoch, rgid FROM guilds WHERE id = ?', gg)
            dd = c.fetchall()
        if table == 'users':
            c.execute('SELECT rowid, * FROM users')
            dd = c.fetchall()
        else:
            e.add_field(name='Error!', value='Table not found')
            await ctx.send(embed=e)
            return
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
                fields == 0
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
        
    
def scrub(table_name):
    x = ''.join( chr for chr in table_name if chr.isalnum() )
    if x == table_name:
        return table_name
    else:
        print("Non-alphanumeric table name detected! Aborting!")
        raise 
    
def setup(bot):
    bot.add_cog(database(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'guilds' ('id' TEXT, 'role' TEXT,'emoch' TEXT, 'rgid' TEXT UNIQUE)")
    c.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER UNIQUE, 'name' TEXT, 'birthday' TEXT, 'location' TEXT, 'timezone' TEXT, 'pronouns' TEXT, 'sexuality' TEXT)")
    conn.commit()
    conn.close
            
    