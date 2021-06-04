import os
import discord
import sqlite3
import random
from discord.ext import commands
from discord.utils import get 
from random import choice

class innout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print('member joined')
        random.seed()
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        guild = self.bot.get_guild(member.guild.id)
        args = (member.guild.id,)
        #c.execute("SELECT role FROM guilds WHERE emoch LIKE '%JOIN' AND id=?", args)
        #for item in c.fetchall():
        #    rol = guild.get_role(int(item[0]))
        #    await discord.Member.add_roles(member, rol)
        #    print('adding role')
        u = member.mention
        titles = ('Hello there', 'Hi', 'Welcome', 'Greetings', 'What\'s poppin', 'Guten tag', 'Bonjour', 'Hola','G\'day mate', 'Hello', 'Hemlo', 'What\'s up mother shucker', 'Sup')
        bodies = (f'{u} has arrived', f'{u} is here to chew ass and kick gum', f'{u} has been summoned', f'{u} materialized', f'{u} has landed', f'All hail {u}', f'{u} fell in', f'{u} slid in', f'{u} has risen from the depths', f'Ah, {u}! Just in time!')
        guild = self.bot.get_guild(member.guild.id)
        e=discord.Embed(title = choice(titles), description = choice(bodies), color = member.color)
        e.set_author(name=f'{member.name} #{member.discriminator}', icon_url=member.avatar_url)
        await guild.system_channel.send(embed=e)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print('Memeber left')
        random.seed()
        u = member.display_name
        titles = ('Farewell', 'Goodbye', 'See you later alligator', 'Adiós', 'Bye', 'See ya','We won\'t miss you', 'Later, nerd', 'See you in hell', 'F')
        bodies = (f'{u} has left the server', f'{u} ditched this shithole', f'{u} succumbed to the heretic ways', f'{u} fucked off', f'{u} dissolved', f'{u} has returned to the soil', f'{u} has gone to Valhalla', f'{u} has been lost to the horde', f'{u} dieded', f'{u} went to Brazil', f'{u} was smited')
        guild = self.bot.get_guild(member.guild.id)
        e=discord.Embed(title = choice(titles), description = choice(bodies), color = member.color)
        async for entry in guild.audit_logs(limit=1):
            if entry.target == member and entry.action == discord.AuditLogAction.kick:
                e=discord.Embed(title = choice(titles), description = 'get kicked loser', color = member.color)
        async for entry in guild.audit_logs(limit=1):
            if entry.target == member and entry.action == discord.AuditLogAction.ban:
                e=discord.Embed(title = choice(titles), description = 'get banned loser', color = member.color)
        e.set_author(name=f'{member.name} #{member.discriminator}', icon_url=member.avatar_url)
        await guild.system_channel.send(embed=e)
        
def setup(bot):
    bot.add_cog(innout(bot))