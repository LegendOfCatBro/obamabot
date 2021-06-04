import os
import discord
import datetime
import sqlite3
from discord.ext import tasks, commands
from datetime import *
from discord.utils import find, get

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.temppunish.start()
    def cog_unload(self):
        self.temppunish.cancel()
    
    @tasks.loop(seconds=60.0)
    async def temppunish(self):
        #initialize databasae
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT * FROM punish WHERE end IS NOT NULL")
        usrs = c.fetchall()
        #for each entry in database, check if its time to free them
        for user in usrs:
            freedomdate = datetime.fromisoformat(user[4])
            now = datetime.utcnow()
            if freedomdate < now:
                #if its time to free them, find who they are, the server theyre in, and the mute role
                guild = self.bot.get_guild(user[0])
                member = guild.get_member(user[1])
                c.execute(f"SELECT value FROM guconfig WHERE id={guild.id} AND job='cancerrole' AND valuetype='ROLE'")
                rid = c.fetchone()[0]
                role = guild.get_role(int(rid))
                #remove trhe role and remove punishment from database
                await discord.Member.remove_roles(member,role)
                unique=f'{guild.id+member.id}cancer'
                c.execute("DELETE FROM punish WHERE uniqueid=?",(unique,))
                #DM the user saying they are unmuted
                if not member.dm_channel:
                    await member.create_dm()
                e = discord.Embed(title="sentence served", description=f"your mute in {guild.name} has expired", color=0x7C0A02)
                await member.dm_channel.send(embed=e)
        conn.commit()
        conn.close()
                    
    @temppunish.before_loop
    async def before_temppunish(self):
        await self.bot.wait_until_ready()
    @commands.check_any(commands.has_permissions(mute_members=True),commands.has_permissions(administrator=True), commands.is_owner())    
    @commands.command(
        name='cancer',
        description='`obama cancer {user ping} [optional:duration]`: sends the user to brazil. duration format: `3d 2h 1m` would cancer for 3 days 2 hours and 1 minute, all three arguments are optional'
    )
    async def cancer(self, ctx, user, *durs):
        #initialize database and check if mute role exists
        conn=sqlite3.connect('bot.db')
        c=conn.cursor()
        c.execute("SELECT value FROM guconfig WHERE job='cancerrole' AND valuetype='ROLE'")
        rid=c.fetchone()[0]
        #if no mute role is found, make one
        if not rid:
            await ctx.guild.create_role(name='cancer', color=discord.Color(0x010101))
            role = find(lambda m: m.position == 1, ctx.guild.roles)
            print('role:')
            print(role)
            rid = role.id
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
            args=(ctx.guild.id,'cancerrole',role.id,'ROLE',str(ctx.guild.id)+'cancerrole')
            c.execute("INSERT INTO guconfig (id, job, value, valuetype, uniqueid) VALUES (?,?,?,?,?)", args)
        #find the user, mute role, and define the unique punishment id as well as the time of punishment  
        rid=int(rid)
        uid=ctx.message.mentions[0].id
        unique=f'{int(ctx.guild.id)+uid}cancer'
        user = await ctx.guild.fetch_member(uid)
        role = ctx.guild.get_role(rid)
        now=datetime.utcnow()
        #if no duration is provided, make it permanent and save that to punishment database
        if not durs:
            push=(ctx.guild.id, uid, 'cancer', now.isoformat(), unique, ctx.guild.id, uid, 'cancer', now.isoformat())
            c.execute("INSERT INTO punish (id, uid, punishment, start, uniqueid) VALUES (?,?,?,?,?) ON CONFLICT(uniqueid) DO UPDATE SET id=?, uid=?, punishment=?, start=?", push)
            print(user)
            print(role)
            await discord.Member.add_roles(user, role)
            await ctx.message.add_reaction('👍')
            conn.commit()
            conn.close
            return
        #if there is a duration, find out what it is 
        for arg in durs:
            t=arg[:-1]
            #if the duration isnt a number then raise an error
            try:
                t=int(t)
            except:
                raise(commands.BadArgument)
            #mark the duration in days hours and minutes
            d=0
            h=0
            m=0
            if arg.lower().endswith('d'):
                d=t
            elif arg.lower().endswith('h'):
                h=t
            elif arg.lower().endswith('m'):
                m=t
            #if the argument is formatted wrong, raise an error
            else:
                raise(commands.BadArgument)
        #use the duration to add to the current time to save the time the punishment will end
        duration = timedelta(days=d, minutes=m, hours=h)
        freedom=now+duration
        #punish the user and commit 
        push=(ctx.guild.id, uid, 'cancer', now.isoformat(), freedom.isoformat(), unique, ctx.guild.id, uid, 'cancer', now.isoformat(), freedom.isoformat())
        c.execute("INSERT INTO punish (id, uid, punishment, start, end, uniqueid) VALUES (?,?,?,?,?,?) ON CONFLICT(uniqueid) DO UPDATE SET id=?, uid=?,punishment=?,start=?,end=?", push)
        await discord.Member.add_roles(user, role)
        await ctx.message.add_reaction('👍')
        conn.commit()
        conn.close
    @commands.check_any(commands.has_permissions(mute_members=True),commands.has_permissions(administrator=True), commands.is_owner())    
    @commands.command(
        name='uncancer',
        description='`obama uncancer {user ping}`: unmutes the mentioned user'
    )
    async def uncancer(self, ctx, user):
        #initialize database and identify user
        conn=sqlite3.connect('bot.db')
        c=conn.cursor()
        uid=ctx.message.mentions[0].id
        user = await ctx.guild.fetch_member(uid)
        c.execute(f"SELECT * FROM punish WHERE id={ctx.guild.id} AND punishment='cancer' AND uid={uid}")
        #if user is not punished, raise an error
        if not c.fetchone():
            raise commands.BadArgument
        #find cancer role
        c.execute(f"SELECT value FROM guconfig WHERE job='cancerrole' AND id={ctx.guild.id} AND valuetype='ROLE'")
        rid = c.fetchone()[0]
        #if no role is found, raise an error
        if not rid:
            raise commands.RoleNotFound
        role = ctx.guild.get_role(int(rid))
        #remove the cancer role and delete punishment from database
        await discord.Member.remove_roles(user,role)
        unique=f'{int(ctx.guild.id)+uid}cancer'
        c.execute("DELETE FROM punish WHERE uniqueid=?",(unique,))
        await ctx.message.add_reaction('👍')
        conn.commit()
        conn.close
   
'''    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #initialize database
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        guild = self.bot.get_guild(payload.guild_id)
        c.execute(f"SELECT value FROM gconfig WHERE job='CANCEREMOJI' AND id={guild.id}")
        #check if the reaction added is the right one
        emo = c.fetchone()
        print(emo)
        emojiflag=0
        for emoji in emo:
            print(emoji)
            print(payload.emoji.name)
            if emoji == payload.emoji.name:
                
                emojiflag = 1
        if not emojiflag:
            return
        #look for mute role
        c.execute("SELECT value FROM guconfig WHERE job='cancerrole' AND valuetype='ROLE'")
        rid=c.fetchone()[0]
        #if no mute role is found, make one
        if not rid:
            await guild.create_role(name='cancer', color=discord.Color(0x010101))
            role = find(lambda m: m.position == 1, guild.roles)
            rid = role.id
            for channel in guild.channels:
                await channel.set_permissions(role, send_messages=False)
            args=(guild.id,'cancerrole',role.id,'ROLE',str(guild.id)+'cancerrole')
            c.execute("INSERT INTO guconfig (id, job, value, valuetype, uniqueid) VALUES (?,?,?,?,?)", args)
        #find information needed for the punishment database
        uid = payload.member.id
        unique=f'{int(guild.id)+uid}cancer'
        user = payload.member
        role = guild.get_role(int(rid))
        now=datetime.utcnow()
        #record the punishment in the database and apply it
        push=(guild.id, uid, 'cancer', now.isoformat(), unique, guild.id, uid, 'cancer', now.isoformat())
        c.execute("INSERT INTO punish (id, uid, punishment, start, uniqueid) VALUES (?,?,?,?,?) ON CONFLICT(uniqueid) DO UPDATE SET id=?, uid=?, punishment=?, start=?", push)
        await discord.Member.add_roles(user, role)
        conn.commit()
        conn.close
      '''  
def setup(bot):
    bot.add_cog(admin(bot))