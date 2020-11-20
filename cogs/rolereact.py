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
        c.execute('SELECT emoch FROM guilds WHERE id=? AND role=?', (str(payload.guild_id),'roles'))
        roid = c.fetchone()
        guild = self.bot.get_guild(payload.guild_id)
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        emo = payload.emoji.name
        c.execute('SELECT role, emoch FROM guilds WHERE id=?', (str(payload.guild_id),))
        emoDict = {}
        for row in c.fetchall():
            emoDict[row[1]] = row[0]
        conn.close
        if roid == (str(payload.channel_id),):
            try:
                g = emoDict[payload.emoji.name]
                rol = guild.get_role(int(g))
                member = payload.member
                await discord.Member.add_roles(member, rol)
            except: 
                react = get(msg.reactions, emoji=payload.emoji.name)
                user = self.bot.get_user(payload.user_id)
                await react.remove(user)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('SELECT emoch FROM guilds WHERE id=? AND role=?', (str(payload.guild_id),'roles'))
        roid = c.fetchone()
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        emo = payload.emoji.name
        c.execute('SELECT role, emoch FROM guilds WHERE id=?', (str(payload.guild_id),))
        emoDict = {}
        for row in c.fetchall():
            emoDict[row[1]] = row[0]
        conn.close
        if roid == (str(payload.channel_id),):
            g = emoDict[payload.emoji.name]
            rol = guild.get_role(int(g))
            await member.remove_roles(rol)

def setup(bot):
    bot.add_cog(rolereact(bot))
    
