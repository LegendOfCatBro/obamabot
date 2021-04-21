import os
import discord
import sqlite3
from discord.ext import commands
from discord.utils import get

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        #change these to your preference 
        starboard_emoji = '⭐'
        starboard_threshold = 3
        starboard_color = 0xF9A602
    
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("SELECT emoch FROM guilds WHERE id=? AND role='starboard'",(str(payload.guild_id),))
        bid = c.fetchone()
        board = self.bot.get_channel(int(bid[0]))
        guild = self.bot.get_guild(payload.guild_id)
        sauce = guild.get_channel(payload.channel_id)
        msg = await sauce.fetch_message(payload.message_id)
        member = msg.author
        goodtypes = ('.png', '.PNG', '.jpg', '.jpeg', '.JPG', '.JPEG', '.gif', '.gifv')
        star = get(msg.reactions, emoji=starboard_emoji)
        c.execute("SELECT role FROM guilds WHERE emoch=? AND id=?", ("🚧", str(payload.guild_id)))
        badmen = c.fetchone()
        badmen = guild.get_role(int(badmen[0]))
        if badmen in member.roles:
            await star.remove(member)
            if not member.dm_channel:
                await member.create_dm()
            e = discord.Embed(title="fuck off", description=f"one of your roles in {guild.name} prevents you from adding stars retard", color=0x7C0A02)
            await member.dm_channel.send(embed=e)
            return
        c.execute("SELECT emoch FROM guilds WHERE emoch=? AND role='starblacklist'",(str(payload.channel_id),))
        if c.fetchone():
            e = discord.Embed(title="fuck off", description="this channel is blacklisted from the starboard retards", color=0x7C0A02)
            await sauce.send(embed=e)
            return
        if payload.emoji.name == starboard_emoji and star.count == starboard_threshold:
            e = discord.Embed(description=msg.content, color=starboard_color)
            e.add_field(name='Sauce', value=f'[Jump!]({msg.jump_url})', inline=False)
            e.set_author(name=msg.author, icon_url=msg.author.avatar_url)
            e.set_footer(text=msg.created_at)
            
            if len(msg.attachments) == 1 and msg.attachments[0].filename.endswith(goodtypes):
                e.set_image(url = msg.attachments[0].url)
                
            elif len(msg.attachments) == 1 and not msg.attachments[0].filename.endswith(goodtypes):
                e.add_field(name='Error!', value='Error adding attachment. Unsupported filetype!')
                print('Error adding starboard attachment: Unsupported filetype!')
                
            elif len(msg.attachments) > 1:
                e.add_field(name='Error!', value='Error adding attachment. Too many attachments!')
                print('Error adding starboard attachment: Too many attachments!')
                
            try:
                await board.send(embed = e)   
            except:
                x = discord.Embed(title='Error!', description='Error sending embed to starboard! The starboard channel ID could be invalid.', color =0x7C0A02) 
                await sauce.send(embed = x)
    @commands.Cog.listener()
    async def on_message(self,payload):
        conn=sqlite3.connect('bot.db')
        c=conn.cursor()
        c.execute("SELECT emoch FROM guilds WHERE id=? AND role='starboard'",(str(payload.guild.id),))
        bid = c.fetchone()
        if not bid:
            pass
        channel = self.bot.get_channel(int(bid[0]))
        member = payload.guild.get_member(self.bot.user.id)
        if payload.channel == channel and not payload.author == member:
            await payload.delete()
            
def setup(bot):
    bot.add_cog(starboard(bot))