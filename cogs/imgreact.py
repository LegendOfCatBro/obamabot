import os
import discord
from discord.ext import commands

class txtreact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        ctx = message.channel
        e = discord.Embed()
        if message.author == self.bot.user:
            return
        elif msg == 'i refuse':
            e.set_image(url='https://i.imgur.com/z4z6pzH.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: i refuse')
        
        elif msg == 'arrivederci':
            e.set_image(url='https://i.imgur.com/q9tOcam.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: arrovederci')
        
        elif msg == 'nice':
            e.set_image(url='https://i.imgur.com/wHZhy5J.png')
            await ctx.send(embed=e)
            print('Reaction triggered: nice')
        
        elif 'go to horny jail' in msg:
            e.set_image(url='https://i.imgur.com/UP56DLT.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: go to horny jail')
        
        elif msg == 'whomst has summoned the almighty one' or msg == 'whomst':
            e.set_image(url='https://i.imgur.com/UTcwmu0.png')
            await ctx.send(embed=e)
            print('Reaction triggered: whomst has summoned the almighty one')
        
        elif msg == 'smol brain':
            e.set_image(url='https://i.imgur.com/RrCXPpX.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: smol brain')
            
        elif msg == 'shut':
            e.set_image(url='https://i.imgur.com/90CweNH.png')
            await ctx.send(embed=e)
            print('Reaction triggered: shut')
        
        elif msg == 'silence':
            e.set_image(url='https://i.imgur.com/HMtP4Ps.png')
            await ctx.send(embed=e)
            print('Reaction triggered: silence')
           
        elif 'loli' in msg:
            e.set_image(url='https://i.imgur.com/7IpEYN1.png')
            await ctx.send(embed=e)
            print('Reaction triggered: loli')
            
        elif 'requiem' in msg:
            e.set_image(url='https://i.imgur.com/OwW4e2M.png')
            await ctx.send(embed=e)
            print('Reaction triggered: requiem')
        
        elif 'owo' in msg:
            e.set_image(url='https://i.redd.it/dm9j0nybble31.png')
            await ctx.send(embed=e)
            print('Reaction triggered: owo')
        
        elif msg == 'delet this':
            e.set_image(url='https://i.ytimg.com/vi/tVEAXcnpgWY/hqdefault.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: delet this')
            
        elif msg.startswith('cease') == True:
            e.set_image(url='https://s.micp.ru/oHhK0.png')
            await ctx.send(embed=e)
            print('Reaction triggered: cease')
        
        elif msg == 'can u dont':
            e.set_image(url='https://s.micp.ru/VN82T.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: can u dont')
        
        elif msg == 'fuck you':
            e.set_image(url='http://ipic.su/img/img7/fs/kiss_299kb.1516859906.png')
            await ctx.send(embed=e)
            print('Reaction triggered: can u dont')
            
        elif msg.startswith('congrat') == True:
            e.set_image(url='https://i.kym-cdn.com/photos/images/newsfeed/000/707/322/fac.gif')
            await ctx.send(embed=e)
            print('Reaction triggered: congrats')
            
        elif 'killer queen' in msg or 'bites the dust' in msg or 'bites za dusto' in msg or 'baitsa dusto' in msg:
            e.set_image(url='https://i.imgur.com/hQRpIVU.png')
            await ctx.send(embed=e)
            print('Reaction triggered: baitsa dusto')
            
        elif msg == 'are you sure about that':
            e.set_image(url='https://thumbs.gfycat.com/CaringSmugInsect-size_restricted.gif')
            await ctx.send(embed=e)
            print('Reaction triggered: are you sure about that')
            
        elif msg == 'doubt':
            e.set_image(url='https://i.imgur.com/8KTtscB.png')
            await ctx.send(embed=e)
            print('Reaction triggered: doubt')
        
        elif msg.startswith('understandable') == True:
            e.set_image(url='http://ipic.su/img/img7/fs/kiss_173kb.1508240578.png')
            await ctx.send(embed=e)
            print('Reaction triggered: understandable')
            
        elif msg == 'how homosexual of you':
            e.set_image(url='https://i.imgur.com/vgKLmYv.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: how homosexual of you')
            
        elif msg.startswith('gonna cry') == True:
            e.set_image(url='https://i.imgur.com/zIgwuck.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: gonna cry')
            
        elif msg.startswith('begone') == True:
            e.set_image(url='https://i.imgur.com/J06iwrc.jpg')
            await ctx.send(embed=e)
            print('Reaction triggered: begone degenerate')
        
        elif 'delete this' in msg:
            e.set_image(url='https://i.imgur.com/f1LX200.png')
            await ctx.send(embed=e)
            print('Reaction triggered: delete this')
            
        elif 'hot milf' in msg:
            e.set_image(url='https://i.imgur.com/W4gr6Zi.gif')
            e.add_field(name='Fuck you ', value='Have a REAL hot MILF', inline=True)
            await ctx.send(embed=e)
            print('Reaction triggered: hot milf')
        
def setup(bot):
    bot.add_cog(txtreact(bot))