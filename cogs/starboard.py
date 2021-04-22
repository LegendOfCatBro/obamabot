import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import get
from discord.utils import find

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        #default settings
        starboard_emoji = '⭐'
        starboard_threshold = 5
        starboard_color = 0xF9A602
        
        #loading custom settings
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT value FROM guconfig WHERE id=? AND job='STARCHANNEL'",(str(payload.guild_id),))
        bid = int(c.fetchone()[0])
        #if there is no starboard channel, ignore everything
        if not bid:
            return
        c.execute("SELECT value FROM guconfig WHERE id=? AND job='STARTHRESHOLD'",(str(payload.guild_id),))
        starboard_threshold = int(c.fetchone()[0])
        c.execute("SELECT value FROM guconfig WHERE id=? AND job='STAREMOJI'",(str(payload.guild_id),))
        starboard_emoji=c.fetchone()[0]
        #finding the channels, message, author, guild, and emoji
        board = self.bot.get_channel(bid)
        guild = self.bot.get_guild(payload.guild_id)
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        member = msg.author
        star = get(msg.reactions, emoji=starboard_emoji)
        #defining list of filetypes that discord embeds support
        goodtypes = ('.png', '.PNG', '.jpg', '.jpeg', '.JPG', '.JPEG', '.gif', '.gifv')
        
        #handles the features for blacklisting a role or channel from the starboard
        c.execute("SELECT value,valuetype FROM gconfig WHERE job='STARBLACKLIST' AND id=?", (str(payload.guild_id),))
        chblist = []
        rblist = []
        for row in c.fetchall():
            types={'ROLE':guild.roles,'CHANNEL':guild.channels}
            item = find(lambda m: m.id == row[0], types[row[1]])
            if row[1]=='CHANNEL':
                chblist.append(item)
            else:
                rblist.append(item)
        if list(set(rblist) & set(member.roles)):
            await star.remove(member)
            if not member.dm_channel:
                await member.create_dm()
            e = discord.Embed(title="fuck off", description=f"one of your roles in {guild.name} prevents you from adding stars retard", color=0x7C0A02)
            await member.dm_channel.send(embed=e)
            return
        if sauce in chblist:
            raise commands.MissingPermissions()
            return
        #checking if the threshold has been passed, and if so, prep the embed
        if payload.emoji.name == starboard_emoji and star.count == starboard_threshold:
            e = discord.Embed(description=msg.content, color=starboard_color)
            e.set_author(name=msg.author, icon_url=msg.author.avatar_url)
            e.set_footer(text=msg.created_at)
            
            
            #adding attachments if possible
            atch = msg.attachments
            if len(atch) == 1 and atch[0].filename.endswith(goodtypes):
                e.set_image(url = atch[0].url)
            elif len(atch) == 1 and not atch[0].filename.endswith(goodtypes):
                e.add_field(name='Unable to embed attachment', value=f'[{atch[0].filename}]({atch[0].url})')

            
            elif len(msg.attachments) > 1:
                links=''
                for attachment in atch:
                    links = links+f'[{attachment.filename}]({attachment.url})   '
                e.add_field(name='Unable to embed attachments', value=f'Unable to embed: {links}')
            #add the jump link at the bottom of the embed
            e.add_field(name='Sauce', value=f'[Jump!]({msg.jump_url})', inline=False)    
            try:
                await board.send(sauce.mention, embed = e)   
            except:
                raise commands.CommandError
    @commands.Cog.listener()
    async def on_message(self,payload):
        conn=sqlite3.connect('bot.db')
        c=conn.cursor()
        c.execute("SELECT value FROM guconfig WHERE id=? AND job='STARCHANNEL'",(str(payload.guild.id),))
        bid = c.fetchone()
        if not bid:
            pass
        channel = self.bot.get_channel(int(bid[0]))
        member = payload.guild.get_member(self.bot.user.id)
        if payload.channel == channel and not payload.author == member:
            await payload.delete()
            
            
def setup(bot):
    bot.add_cog(starboard(bot))