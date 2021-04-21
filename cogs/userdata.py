import discord
import sqlite3
import threading
import random
from discord.ext import tasks, commands
from discord.utils import find
from datetime import datetime
from datetime import date
from pytz import timezone
from pytz import common_timezones
from random import choice

class userdata(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.bday.start()
    def cog_unload(self):
        self.bday.cancel()
    
    @tasks.loop(seconds=60.0)
    async def bday(self):
        conn=sqlite3.connect('bot.db')
        c=conn.cursor()
        c.execute("SELECT id,timezone,birthday FROM users")
        usrs = c.fetchall()
        for user in usrs:
            if user[2]:
                bday = date.fromisoformat(user[2]).replace(year=datetime.now().date().year)
                if user[1]:
                    t1 = datetime.now(timezone(user[1]))
                    today = t1.date()
                    now = f'{t1.hour}:{t1.minute}'
                else:
                    t2 = datetime.now()
                    today = t2.date()
                    now = f'{t2.hour}:{t2.minute}'
                if today == bday and now == '9:11':
                    c.execute("SELECT * FROM guilds WHERE role='bday'")
                    glds = c.fetchall()
                    for guld in glds:
                        guild = self.bot.get_guild(int(guld[0]))
                        if guild.get_member(user[0]):
                            ch = guild.get_channel(int(guld[2]))
                            titles=('happy bitchday', 'happy your parents fucked 9 months ago', 'pleasant anniversarry of your birth', 'one year closer to the sweet release of death')
                            images=('https://images-ext-2.discordapp.net/external/oq_t8Mr3ubuXm56iu3ZYvQiBAC7L_y6vd30CdOMDM_s/https/apocake.files.wordpress.com/2020/01/cake-13.jpg?width=524&height=684',
                                    'https://media.discordapp.net/attachments/718134843455832095/789982106108297226/image0.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789982131413581865/image0.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789987686340755466/cakes-with-threatening-auras-23-5f4d0323bf3d7__700.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789987637606875136/cakes-with-threatening-auras.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789987567939616808/EDOk8n2XoAE7R3G.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789987462302269450/5-cursed-cakes-1599150988834.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789987436842188830/4uujjq9n9w611.png?width=553&height=684',
                                    'https://media.discordapp.net/attachments/718134843455832095/789988015438037022/7bcd064e91a915f99722d55e438871ef.png',
                                    'https://media.discordapp.net/attachments/718134843455832095/789988066068529162/cakes-with-threatening-auras-45-5f4d034fb3b74__700.png'
                                    )
                            random.seed()
                            mbmr = guild.get_member(user[0])
                            colr = random.randint(0, 0xffffff)
                            e = discord.Embed(title=choice(titles), description=f'It is {mbmr.mention}\'s birthday !', color=colr)
                            img = choice(images)
                            print(img)
                            e.set_image(url=img)
                            await ch.send(embed=e)
    @bday.before_loop
    async def before_bday(self):
        print('waiting...')
        await self.bot.wait_until_ready()
    @commands.command(
        name='timezones',
        description='Show information on timezones that can be bound to your profile!'
    )
    async def timezones(self, ctx, *args):
        if not args:
            x = discord.Embed(title='Please specify a region',description=f'Africa\nAmericas\nAustralia\nEurope\nAsia\nOcean\nAntarctic/Arctic',color=ctx.author.color)
            await ctx.send(embed=x)
            return
        tzdict = {
            'africa':'Africa/Abidjan\nAfrica/Accra\nAfrica/Addis_Ababa\nAfrica/Algiers\nAfrica/Asmara\nAfrica/Bamako\nAfrica/Bangui\nAfrica/Banjul\nAfrica/Bissau\nAfrica/Blantyre\nAfrica/Brazzaville\nAfrica/Bujumbura\nAfrica/Cairo\nAfrica/Casablanca\nAfrica/Ceuta\nAfrica/Conakry\nAfrica/Dakar\nAfrica/Dar_es_Salaam\nAfrica/Djibouti\nAfrica/Douala\nAfrica/El_Aaiun\nAfrica/Freetown\nAfrica/Gaborone\nAfrica/Harare\nAfrica/Johannesburg\nAfrica/Juba\nAfrica/Kampala\nAfrica/Khartoum\nAfrica/Kigali\nAfrica/Kinshasa\nAfrica/Lagos\nAfrica/Libreville\nAfrica/Lome\nAfrica/Luanda\nAfrica/Lubumbashi\nAfrica/Lusaka\nAfrica/Malabo\nAfrica/Maputo\nAfrica/Maseru\nAfrica/Mbabane\nAfrica/Mogadishu\nAfrica/Monrovia\nAfrica/Nairobi\nAfrica/Ndjamena\nAfrica/Niamey\nAfrica/Nouakchott\nAfrica/Ouagadougou\nAfrica/Porto-Novo\nAfrica/Sao_Tome\nAfrica/Tripoli\nAfrica/Tunis\nAfrica/Windhoek',
            'australia':'Australia/Adelaide\nAustralia/Brisbane\nAustralia/Broken_Hill\nAustralia/Currie\nAustralia/Darwin\nAustralia/Eucla\nAustralia/Hobart\nAustralia/Lindeman\nAustralia/Lord_Howe\nAustralia/Melbourne\nAustralia/Perth\nAustralia/Sydney',
            'europe':'Europe/Amsterdam\nEurope/Andorra\nEurope/Astrakhan\nEurope/Athens\nEurope/Belgrade\nEurope/Berlin\nEurope/Bratislava\nEurope/Brussels\nEurope/Bucharest\nEurope/Budapest\nEurope/Busingen\nEurope/Chisinau\nEurope/Copenhagen\nEurope/Dublin\nEurope/Gibraltar\nEurope/Guernsey\nEurope/Helsinki\nEurope/Isle_of_Man\nEurope/Istanbul\nEurope/Jersey\nEurope/Kaliningrad\nEurope/Kiev\nEurope/Kirov\nEurope/Lisbon\nEurope/Ljubljana\nEurope/London\nEurope/Luxembourg\nEurope/Madrid\nEurope/Malta\nEurope/Mariehamn\nEurope/Minsk\nEurope/Monaco\nEurope/Moscow\nEurope/Oslo\nEurope/Paris\nEurope/Podgorica\nEurope/Prague\nEurope/Riga\nEurope/Rome\nEurope/Samara\nEurope/San_Marino\nEurope/Sarajevo\nEurope/Saratov\nEurope/Simferopol\nEurope/Skopje\nEurope/Sofia\nEurope/Stockholm\nEurope/Tallinn\nEurope/Tirane\nEurope/Ulyanovsk\nEurope/Uzhgorod\nEurope/Vaduz\nEurope/Vatican\nEurope/Vienna\nEurope/Vilnius\nEurope/Volgograd\nEurope/Warsaw\nEurope/Zagreb\nEurope/Zaporozhye\nEurope/Zurich',
            'asia':'Asia/Aden\nAsia/Almaty\nAsia/Amman\nAsia/Anadyr\nAsia/Aqtau\nAsia/Aqtobe\nAsia/Ashgabat\nAsia/Atyrau\nAsia/Baghdad\nAsia/Bahrain\nAsia/Baku\nAsia/Bangkok\nAsia/Barnaul\nAsia/Beirut\nAsia/Bishkek\nAsia/Brunei\nAsia/Chita\nAsia/Choibalsan\nAsia/Colombo\nAsia/Damascus\nAsia/Dhaka\nAsia/Dili\nAsia/Dubai\nAsia/Dushanbe\nAsia/Famagusta\nAsia/Gaza\nAsia/Hebron\nAsia/Ho_Chi_Minh\nAsia/Hong_Kong\nAsia/Hovd\nAsia/Irkutsk\nAsia/Jakarta\nAsia/Jayapura\nAsia/Jerusalem\nAsia/Kabul\nAsia/Kamchatka\nAsia/Karachi\nAsia/Kathmandu\nAsia/Khandyga\nAsia/Kolkata\nAsia/Krasnoyarsk\nAsia/Kuala_Lumpur\nAsia/Kuching\nAsia/Kuwait\nAsia/Macau\nAsia/Magadan\nAsia/Makassar\nAsia/Manila\nAsia/Muscat\nAsia/Nicosia\nAsia/Novokuznetsk\nAsia/Novosibirsk\nAsia/Omsk\nAsia/Oral\nAsia/Phnom_Penh\nAsia/Pontianak\nAsia/Pyongyang\nAsia/Qatar\nAsia/Qostanay\nAsia/Qyzylorda\nAsia/Riyadh\nAsia/Sakhalin\nAsia/Samarkand\nAsia/Seoul\nAsia/Shanghai\nAsia/Singapore\nAsia/Srednekolymsk\nAsia/Taipei\nAsia/Tashkent\nAsia/Tbilisi\nAsia/Tehran\nAsia/Thimphu\nAsia/Tokyo\nAsia/Tomsk\nAsia/Ulaanbaatar\nAsia/Urumqi\nAsia/Ust-Nera\nAsia/Vientiane\nAsia/Vladivostok\nAsia/Yakutsk\nAsia/Yangon\nAsia/Yekaterinburg\nAsia/Yerevan',
            'ocean':'Indian/Antananarivo\nIndian/Chagos\nIndian/Christmas\nIndian/Cocos\nIndian/Comoro\nIndian/Kerguelen\nIndian/Mahe\nIndian/Maldives\nIndian/Mauritius\nIndian/Mayotte\nIndian/Reunion\nAtlantic/Azores\nAtlantic/Bermuda\nAtlantic/Canary\nAtlantic/Cape_Verde\nAtlantic/Faroe\nAtlantic/Madeira\nAtlantic/Reykjavik\nAtlantic/South_Georgia\nAtlantic/St_Helena\nAtlantic/Stanley\nPacific/Apia\nPacific/Auckland\nPacific/Bougainville\nPacific/Chatham\nPacific/Chuuk\nPacific/Easter\nPacific/Efate\nPacific/Enderbury\nPacific/Fakaofo\nPacific/Fiji\nPacific/Funafuti\nPacific/Galapagos\nPacific/Gambier\nPacific/Guadalcanal\nPacific/Guam\nPacific/Honolulu\nPacific/Kiritimati\nPacific/Kosrae\nPacific/Kwajalein\nPacific/Majuro\nPacific/Marquesas\nPacific/Midway\nPacific/Nauru\nPacific/Niue\nPacific/Norfolk\nPacific/Noumea\nPacific/Pago_Pago\nPacific/Palau\nPacific/Pitcairn\nPacific/Pohnpei\nPacific/Port_Moresby\nPacific/Rarotonga\nPacific/Saipan\nPacific/Tahiti\nPacific/Tarawa\nPacific/Tongatapu\nPacific/Wake\nPacific/Wallis',
            'antarctic/arctic':'Antarctica/Casey\nAntarctica/Davis\nAntarctica/DumontDUrville\nAntarctica/Macquarie\nAntarctica/Mawson\nAntarctica/McMurdo\nAntarctica/Palmer\nAntarctica/Rothera\nAntarctica/Syowa\nAntarctica/Troll\nAntarctica/Vostok\n Arctic/Longyearbyen',
            'americas':'US/Alaska\nUS/Arizona\nUS/Central\nUS/Eastern\nUS/Hawaii\nUS/Mountain\nUS/Pacific\n \nCanada/Atlantic\nCanada/Central\nCanada/Eastern\nCanada/Mountain\nCanada/Newfoundland\nCanada/Pacific',
            'americas2':'America/Adak\nAmerica/Anchorage\nAmerica/Anguilla\nAmerica/Antigua\nAmerica/Araguaina\nAmerica/Argentina/Buenos_Aires\nAmerica/Argentina/Catamarca\nAmerica/Argentina/Cordoba\nAmerica/Argentina/Jujuy\nAmerica/Argentina/La_Rioja\nAmerica/Argentina/Mendoza\nAmerica/Argentina/Rio_Gallegos\nAmerica/Argentina/Salta\nAmerica/Argentina/San_Juan\nAmerica/Argentina/San_Luis\nAmerica/Argentina/Tucuman\nAmerica/Argentina/Ushuaia\nAmerica/Aruba\nAmerica/Asuncion\nAmerica/Atikokan\nAmerica/Bahia\nAmerica/Bahia_Banderas\nAmerica/Barbados\nAmerica/Belem\nAmerica/Belize\nAmerica/Blanc-Sablon\nAmerica/Boa_Vista\nAmerica/Bogota\nAmerica/Boise\nAmerica/Cambridge_Bay\nAmerica/Campo_Grande\nAmerica/Cancun\nAmerica/Caracas\nAmerica/Cayenne\nAmerica/Cayman\nAmerica/Chicago\nAmerica/Chihuahua\nAmerica/Costa_Rica\nAmerica/Creston\nAmerica/Cuiaba\nAmerica/Curacao\nAmerica/Danmarkshavn\nAmerica/Dawson\nAmerica/Dawson_Creek\nAmerica/Denver\nAmerica/Detroit\nAmerica/Dominica\nAmerica/Edmonton\nAmerica/Eirunepe\nAmerica/El_Salvador\nAmerica/Fort_Nelson\nAmerica/Fortaleza\nAmerica/Glace_Bay\nAmerica/Goose_Bay\nAmerica/Grand_Turk\nAmerica/Grenada\nAmerica/Guadeloupe\nAmerica/Guatemala\nAmerica/Guayaquil\nAmerica/Guyana\nAmerica/Halifax\nAmerica/Havana\nAmerica/Hermosillo\nAmerica/Indiana/Indianapolis\nAmerica/Indiana/Knox\nAmerica/Indiana/Marengo\nAmerica/Indiana/Petersburg\nAmerica/Indiana/Tell_City\nAmerica/Indiana/Vevay\nAmerica/Indiana/Vincennes\nAmerica/Indiana/Winamac\nAmerica/Inuvik\nAmerica/Iqaluit',
            'americas3':'America/Jamaica\nAmerica/Juneau\nAmerica/Kentucky/Louisville\nAmerica/Kentucky/Monticello\nAmerica/Kralendijk\nAmerica/La_Paz\nAmerica/Lima\nAmerica/Los_Angeles\nAmerica/Lower_Princes\nAmerica/Maceio\nAmerica/Managua\nAmerica/Manaus\nAmerica/Marigot\nAmerica/Martinique\nAmerica/Matamoros\nAmerica/Mazatlan\nAmerica/Menominee\nAmerica/Merida\nAmerica/Metlakatla\nAmerica/Mexico_City\nAmerica/Miquelon\nAmerica/Moncton\nAmerica/Monterrey\nAmerica/Montevideo\nAmerica/Montserrat\nAmerica/Nassau\nAmerica/New_York\nAmerica/Nipigon\nAmerica/Nome\nAmerica/Noronha\nAmerica/North_Dakota/Beulah\nAmerica/North_Dakota/Center\nAmerica/North_Dakota/New_Salem\nAmerica/Nuuk\nAmerica/Ojinaga\nAmerica/Panama\nAmerica/Pangnirtung\nAmerica/Paramaribo\nAmerica/Phoenix\nAmerica/Port-au-Prince\nAmerica/Port_of_Spain\nAmerica/Porto_Velho\nAmerica/Puerto_Rico\nAmerica/Punta_Arenas\nAmerica/Rainy_River\nAmerica/Rankin_Inlet\nAmerica/Recife\nAmerica/Regina\nAmerica/Resolute\nAmerica/Rio_Branco\nAmerica/Santarem\nAmerica/Santiago\nAmerica/Santo_Domingo\nAmerica/Sao_Paulo\nAmerica/Scoresbysund\nAmerica/Sitka\nAmerica/St_Barthelemy\nAmerica/St_Johns\nAmerica/St_Kitts\nAmerica/St_Lucia\nAmerica/St_Thomas\nAmerica/St_Vincent\nAmerica/Swift_Current\nAmerica/Tegucigalpa\nAmerica/Thule\nAmerica/Thunder_Bay\nAmerica/Tijuana\nAmerica/Toronto\nAmerica/Tortola\nAmerica/Vancouver\nAmerica/Whitehorse\nAmerica/Winnipeg\nAmerica/Yakutat\nAmerica/Yellowknife'
        }
        if args[0].lower() in tzdict.keys():
            x = discord.Embed(title=f'Timezones for region {args[0]}',description=tzdict[args[0]],color=ctx.author.color)  
        else:
            x=discord.Embed(title='Error!',description='Not a valid region!',color=ctx.author.color)
            await ctx.send(embed=x)
        if args[0].lower() == 'americas':
            x.add_field(name='List wes too long, showing US and Canada',value='Do \'obama timezones americas2\' and \'americas3\' to view the full list')
        await ctx.send(embed=x)
        
    @commands.command(
        name='bind',
        desciption='Adds something to your user data'
    )
    async def bind(self, ctx, column, *, args):
        conn=sqlite3.connect('bot.db')
        c = conn.cursor()
        simplecolumns = ("name", "location", "pronouns", "sexuality")
        if column.lower() in simplecolumns:
            arg = (ctx.author.id, args, args)
            c.execute(f"INSERT INTO users (id, {column.lower()}) VALUES (?,?) ON CONFLICT(id) DO UPDATE SET {column.lower()}=?", arg)
            print("bind successful")
            x = discord.Embed(title='binding successful',description=f'{args} bound to {column}',color=ctx.author.color) 
            await ctx.send(embed = x)
        elif column.lower() == 'birthday':
            fmt = "%m/%d/%Y"
            try:
                date = datetime.strptime(args, fmt).date()
                print(date)
            except:
                x = discord.Embed(title='error',description=f'error parsing date: remember to use MM/DD/YYYY format',color=ctx.author.color) 
                await ctx.send(embed = x)
                return
            arg = (ctx.author.id, date, date)
            c.execute(f"INSERT INTO users (id,  birthday) VALUES (?,?) ON CONFLICT(id) DO UPDATE SET birthday=?", arg)
            print("bind successful")
            x = discord.Embed(title='binding successful',description=f'{args} bound to {column}',color=ctx.author.color) 
            await ctx.send(embed = x)    
        elif column.lower() == 'timezone':
            if args in common_timezones:
                arg = (ctx.author.id, args, args)
                c.execute(f"INSERT INTO users (id, timezone) VALUES (?,?) ON CONFLICT(id) DO UPDATE SET timezone=?", arg)
                print("bind successful")
                x = discord.Embed(title='binding successful',description=f'{args} bound to {column}',color=ctx.author.color) 
                await ctx.send(embed = x)
            else:
                x = discord.Embed(title='Error!',description=f'Unable to identify timezone! Try \'obama timezones\' for more information on timezones I know. Timezones are case sensitive!',color=ctx.author.color)
                await ctx.send(embed=x)
        else:
            print('Invalid column')        
        conn.commit()
        conn.close
    
    @commands.command(
        name='unbind',
        desciption='Removes the given item from your user data'
    )
    async def unbind(self, ctx, column):
        conn=sqlite3.connect('bot.db')
        c = conn.cursor()
        if not column.isalnum:
            x = discord.Embed(title='Error!',description=f'Attribute name must be alphanumeric!',color=ctx.author.color)
            await ctx.send(embed=x)
            return
        try:
            c.execute(f"UPDATE users SET {column}=NULL WHERE id={ctx.author.id}")
        except:
            x = discord.Embed(title='Error!',description=f'Invalid Attribute!',color=ctx.author.color)
            await ctx.send(embed=x)
            return
        x = discord.Embed(title='Unbind successful',description=f'Successfully removed data for {column}',color=ctx.author.color)
        await ctx.send(embed=x)
        conn.commit()
        conn.close
    @commands.command(
        name='ui',
        description='View someone\'s info'
    )
    async def ui(self, ctx, *args):
        conn=sqlite3.connect('bot.db')
        c = conn.cursor()
        if not args:
            uid = (ctx.author.id,)
            uid2 = (ctx.author.id)
        elif len(ctx.message.mentions) == 1:
            uid = (ctx.message.mentions[0].id,)
            uid2 = (ctx.message.mentions[0].id)
        else:
            x = discord.Embed(title='error',description=f'unable to find user-- just ping them you dunce, or leave blank to get your own data',color=ctx.author.color)
            await ctx.send(embed=x)
            return
        user = await ctx.guild.fetch_member(uid2)
        c.execute("SELECT * FROM users WHERE id=?", uid)
        data = (c.fetchone())
        if not data:
            x = discord.Embed(title='error',description=f'unable to find data for user-- they probably dont have any data',color=ctx.author.color)
            await ctx.send(embed=x)
            return
        e = discord.Embed(title=f'User data for {user.name}:', color=ctx.author.color)
        if data[4]:
            fmt = "%I:%M %p"
            now_time = datetime.now(timezone(data[4]))
            time=f'{data[4]}\n[Current time: {now_time.strftime(fmt)}]'
        else:
            time='None'
        if data[2]:
            today = date.today()
            bd = date.fromisoformat(data[2]).replace(year=today.year)
            if bd < today:
                bd = bd.replace(year=today.year+1)
            dis = abs(bd-today)
            dis = f'{data[2]}\n[{abs(bd-today).days} days away]'
        else:
            dis='None'
        e.add_field(name='Name', value=data[1])
        e.add_field(name='Birthday', value=dis)
        e.add_field(name='Location', value=data[3])
        e.add_field(name='Timezone', value=time)
        e.add_field(name='Pronouns', value=data[5])
        e.add_field(name='Sexuality', value=data[6])
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)  
    @commands.command(
        name='setrole',
        desciption='Alters your custom role'
    )
    async def setrole(self, ctx, name, color):
        conn=sqlite3.connect('bot.db')
        c=conn.cursor()
        uid=ctx.author.id
        gid=ctx.guild.id
        guild=ctx.guild
        user=ctx.author
        ugid=f'{uid}x{gid}'
        c.execute("SELECT * FROM guilds WHERE emoch='roleanchor😊'")
        if not c.fetchone():
            e=discord.Embed(title=f'That feature has not been set up in this server!', color=ctx.author.color)
            await ctx.send(embed=e)
            return
        c.execute(f'SELECT * FROM userroles WHERE ugid={ugid}')
        g=c.fetchone()
        if g:
            rid=g[2]
            role = guild.get_role(int(rid))
            await role.edit(name=name,color=discord.Color(int(color, 16)))
        else:
            c.execute("SELECT * FROM guilds WHERE emoch='roleanchor😊'")
            f=c.fetchone()[1]
            anchor = guild.get_role(int(f))
            await guild.create_role(name=name, color=discord.Color(int(color, 16)))
            role = guild.get_role(int(f))
            pos=role.position-1
            role = find(lambda m: m.position == 1, ctx.guild.roles)
            rid =role.id
            await role.edit(position=pos)
        arg=(name,color,name,color)
        c.execute(f"INSERT INTO userroles (uid, gid, rid, rname, color, ugid) VALUES ({uid},{gid},{rid}, ?,?,{ugid}) ON CONFLICT(ugid) DO UPDATE SET rname=?, color=?", arg)
        conn.commit()
        conn.close
        await discord.Member.add_roles(user, role)
            
           
def setup(bot):
    bot.add_cog(userdata(bot))