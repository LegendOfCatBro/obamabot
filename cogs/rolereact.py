import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import get


class rolereact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT roleid FROM guilds WHERE gid=?', (str(payload.guild_id),))
        roid = c.fetchone()
        guild = self.bot.get_guild(payload.guild_id)
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        emo = payload.emoji.name
        c.execute('SELECT emo, rid FROM roles WHERE gid=?', (str(payload.guild_id),))
        emoDict = {}
        for row in c.fetchall():
            emoDict[row[0]] = row[1]
        conn.close
        if roid == (str(payload.channel_id),):
            try:
                g = emoDict[payload.emoji.name]
                rol = guild.get_role(int(g))
                member = payload.member
                await discord.Member.add_roles(member, rol)
            except:
                try: 
                    react = get(msg.reactions, emoji=payload.emoji.name)
                    user = self.bot.get_user(payload.user_id)
                    await react.remove(user)
                except:
                    react = get(msg.reactions, emoji=payload.emoji)
                    user = self.bot.get_user(payload.user_id)
                    await react.remove(user)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT roleid FROM guilds WHERE gid=?', (str(payload.guild_id),))
        roid = c.fetchone()
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        emo = payload.emoji.name
        c.execute('SELECT emo, rid FROM roles WHERE gid=?', (str(payload.guild_id),))
        emoDict = {}
        for row in c.fetchall():
            emoDict[row[0]] = row[1]
        conn.close
        if roid == (str(payload.channel_id),):
            try:
                g = emoDict[payload.emoji.name]
                rol = guild.get_role(int(g))
                await member.remove_roles(rol)
            except:
                pass

def setup(bot):
    bot.add_cog(rolereact(bot))
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    for guild in bot.guilds:
        gnt = str(guild.name)
        git = str(guild.id)
        c.execute("CREATE TABLE IF NOT EXISTS 'roles' ('id' INTEGER,'gid' TEXT,'eid' TEXT, 'rid' TEXT,PRIMARY KEY('id'))")
    conn.commit()
    conn.close
