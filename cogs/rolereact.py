import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import get
from discord.utils import find

class rolereact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
       
        rolereact_color = 0xF9A602
        
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT roleid FROM guilds WHERE gid=?', (str(payload.guild_id),))
        guild = self.bot.get_guild(payload.guild_id)
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        
        if c.fetchone() == (str(payload.channel_id),):
            print('Reaction detected in roles channel!')
            
            
            
            
def setup(bot):
    bot.add_cog(rolereact(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    for guild in bot.guilds:
        gnt = str(guild.name)
        git = str(guild.id)
        c.execute("CREATE TABLE IF NOT EXISTS 'guilds' ('ID' INTEGER,'gid' TEXT UNIQUE,'gname' TEXT,'starid' TEXT,'roleid' TEXT,PRIMARY KEY('ID'))")
    conn.commit()
    conn.close
            