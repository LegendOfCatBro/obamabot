import os
import discord
import random
from discord.ext import commands


class rng(commands.Cog):
    def __init__(self, bot):
        self.bot = bot   
    @commands.command(name='roll', description='roll some virtual dice. Supports multiple types of dice and modifiers!')
    async def roll2(self, ctx, *, args):
        embed = discord.Embed(title='Dice Roll', color=ctx.author.color)
        arg = args.split(' ')
        dices = []
        pmod = []
        nmod = []
        errors = 0
        for x in arg:
            f = x.split('d')
            g = x[1:]
            if "d" in x and len(x) > 2 and len(f) == 2 and IsInt(f[0]) == True and IsInt(f[1]) == True and int(f[0]) > 0 and int(f[1]) > 0:
                dices.append(x)
            elif x.startswith('+') == True and len(x) > 1 and IsInt(g) == True:
                pmod.append(int(x[1:]))
            elif x.startswith('-') == True and len(x) > 1 and IsInt(g) == True:
                nmod.append(int(x[1:]))
            elif errors == 24:
                embed.add_field(name='AAAAAAAAAAA', value='TOO MANY ERRORS JESUS FUCKING CHRIST JUST TRY AGAIN')
                await ctx.send(embed=embed)
                return
            else:
                embed.add_field(name='Error!', value=f'Invalid argument {x}, ignoring!')
                errors +=1
        bkdns = []
        sum = 0
        
        if dices:
            for y in dices:
                random.seed()
                dice = y.split('d')
                a = int(dice[0])
                b = int(dice[1])
                s = 0
                bstr = f'({a}d{b}): '
                nums = []
                for x in range(a):
                    t = random.randint(1,b)
                    nums.append(t)
                    bstr += f'{t}, '
                for x in nums:
                    s = x + s
                bstr = bstr[:-2]
                bstr += f' [{s}]'
                sum = sum + s
                bkdns.append(bstr)
            bd = 'Breakdown: {'
            for x in bkdns:
                bd += f'{x} '
            bd = bd[:-1]
            bd += '}'
            bd += f'={sum}'
        else: 
            embed.add_field(name='Error!', value='No valid rolls given! Remember to use the format XdY, with X being the number of dice and Y being the number of sides on each die.')
            await ctx.send(embed=embed)
            return
        if pmod or nmod:
            bd += f'; {sum} '
            for x in pmod:
                bd += f'+{x} '
                sum = sum + x
            for x in nmod:
                bd += f'-{x} '
                sum = sum - x
            bd += f'= {sum}'   
        embed.add_field(name=f'You rolled {sum}!', value=bd)
        await ctx.send(embed=embed)
    @commands.command(name='oracle', description='Ask obama to solve your problems')
    async def oracle(self, ctx, *, args):
        print('oracle')


def setup(bot):
    bot.add_cog(rng(bot))
def IsInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False