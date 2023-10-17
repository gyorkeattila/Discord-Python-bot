from typing import AsyncIterator, DefaultDict
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Intents
from discord import Streaming
from discord.message import Message
from discord.utils import get
from discord.ext import commands
from discord.ext import commands
from discord.utils import get
from datetime import datetime as dt
import datetime 
import asyncio
import random

intents = discord.Intents.all() 
client = commands.Bot(command_prefix='=', intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    global indulas
    indulas = datetime.datetime.now()
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CloudForest"))
    print('Szia Uram')

async def ch_pr():
 await client.wait_until_ready()

 statuses = ["CloudForest",f"Jelenleg aktív: {len(client.guilds)} szerveren","Segítségedre van szügséged? Használd a =help parancsot!"]

 while not client.is_closed():

   status = random.choice(statuses)

   await client.change_presence(activity=discord.Game(name=status))

   await asyncio.sleep(5)

client.loop.create_task(ch_pr())

#Egyedi help parancs
@client.command()
async def help(ctx):
     help_embed = discord.Embed(title="Az összes parancs a bothoz" , description="", color=discord.Color.blue())

     help_embed.set_author (name="Wenseron bot")
     help_embed.add_field(name="Adminisztrátori parancsok", value="", inline=False)
     help_embed.add_field(name="ban", value="A bot pingjének lekérdezése.", inline=False)
     help_embed.add_field(name="unban", value="A bot pingjének lekérdezése.", inline=False)
     help_embed.add_field(name="kick", value="A bot pingjének lekérdezése.", inline=False)
     help_embed.add_field(name="rank", value="Átmenetileg nem működik", inline=False)
     help_embed.add_field(name="clean", value="A bot pingjének lekérdezése.", inline=False)
     help_embed.add_field(name="User parancsok", value="", inline=False)
     help_embed.add_field(name="ping", value="A bot pingjének lekérdezése.", inline=False)
     help_embed.add_field(name="avatar", value="Adott felhasználó avatárjának lekérdezése", inline=False)
     help_embed.add_field(name="botinfo", value="Alap információk a botról", inline=False)
     help_embed.add_field(name="userinfo", value="Az adott felhasználó információi", inline=False)

     
     help_embed.set_footer(text=f"Lekérezte: {ctx.author}", icon_url=ctx.author.avatar)

     await ctx.send(embed=help_embed)   

#ban 
@client.command()
@has_permissions(administrator=True)
async def ban(ctx, *, user:discord.Member,reason="nincs indok"):
    await user.ban(reason=reason) 
    embed = discord.Embed(title=f"{user.name} ki lett bannolva {ctx.guild.name}, indok: {reason}",description=f"Bannolta {ctx.message.author}" , color=discord.Color.blue())
    await ctx.channel.send(embed = embed)
    await ctx.channel.send("https://c.tenor.com/Kt1irdU_daUAAAAC/ban-admin.gif")

@ban.error
async def ban_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}", color=discord.Color.blue())
        await ctx.send(embed = embed)
    ban_error.set_footer(text=f"Lekérezte: {ctx.author}", icon_url=ctx.author.avatar)

#kick
@client.command()
@has_permissions(administrator=True)
async def kick(ctx, *, user:discord.Member,reason="nincs indok"):
    await user.kick(reason=reason) 
    embed = discord.Embed(title=f"{user.name} ki lett rúgva {ctx.guild.name}, indok: {reason}",description=f"Kirúgta {ctx.message.author}")
    await ctx.channel.send(embed = embed)

@kick.error
async def kick_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}", color=discord.Color.blue())
        await ctx.send(embed = embed)


#unban
@client.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
             await ctx.guild.unban(user)
             await ctx.channel.send(f"Ban feloldva: {user.mention}-nak/nek")

@unban.error
async def unban_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}", color=discord.Color.blue())
        await ctx.send(embed = embed)



#ping
@client.command()
async def ping(ctx):
        embedVar = discord.Embed(title="Bot válaszideje", color=discord.Color.blue())
        embedVar.add_field(name="Válaszidő", value=f'{round(client.latency * 1000)}ms', inline=False)
        embedVar.set_footer(text=f"Lekérezte: {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.channel.send(embed=embedVar) 
        


#uptime
@client.command()
async def uptime(ctx):
    now = datetime.datetime.now()
    uptime = indulas - now
    uptime = datetime.timedelta.strftime(uptime, '%d nap %H óra %M perc %S másodperc')
    embedVar = discord.Embed(title="Bot futási ideje")
    embedVar.add_field(name="Idő", value = uptime, inline=False)
    await ctx.channel.send(embed=embedVar)



#avatar
@client.command(aliases=['av'])
async def avatar(ctx,user:discord.Member=None, color=discord.Color.blue()):
    if not user:
        user = ctx.message.author
    embed = discord.Embed()
    embed.set_image(url=user.avatar.url)
    embed.set_footer(text=f"Lekérezte: {ctx.author}", icon_url=ctx.author.avatar)
    await ctx.channel.send(embed = embed)
    


#rangadó
@client.command()
@has_permissions(administrator=True)
async def rank(ctx, user: discord.Member, *, role: discord.Role ):
    rangembed = discord.Embed(title=f"A kért rangot sikeresen hozzá adtam az adott felhasználóhoz")
    rangembed.set_footer(text=f"A rangot hozzáadta: {ctx.author}", icon_url=ctx.author.avatar)
    await user.add_roles(role)
    await ctx.channel.send(embed=rangembed)

#rank hiba
@rank.error
async def rank_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}")
        await ctx.send(embed = embed)
    
#clean
@client.command()
@has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()
        

@clean.error
async def clean_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}")
        await ctx.send(embed = embed) 

   

#botinfo
@client.command()
async def botinfo(ctx):
     tulaj_embed = discord.Embed(color=discord.Color.blue())
     tulaj_embed.set_author (name="A Botot készítette: wenseron")
     tulaj_embed.add_field (name="Weblapot készítette: lildariusz", value="", inline=False)
     tulaj_embed.add_field (name="Futási környezet Python 3.9", value="", inline=False)
     tulaj_embed.set_footer(text=f"Lekérezte: {ctx.author}", icon_url=ctx.author.avatar)
     
     await ctx.send(embed=tulaj_embed)
     

#userinfo
@client.command()
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member

    info_embed = discord.Embed(title=f"{member.name} Felhasználói profilja,", description="", color=discord.Color.blue())
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name="Név", value=member, inline=False)
    info_embed.add_field(name="Becenév", value=member.display_name, inline=False)
    info_embed.add_field(name="ID", value=member.id, inline=False)
    info_embed.add_field(name="Legmagasabb rang", value=member.top_role, inline=False)
    info_embed.add_field(name="Státusz", value=member.status, inline=False)
    info_embed.add_field(name="Bot felhasználó-e?", value=member.bot, inline=False)
    info_embed.add_field(name="A szerverhez csatlakozott", value=member.joined_at.__format__(" %Y/%m/%d %H:%M:%S "), inline=False)
    info_embed.add_field(name="Account létrehozási ideje", value=member.created_at.__format__(" %Y/%m/%d %H:%M:%S "), inline=False)
    info_embed.set_footer(text=f"Lekérezte: {ctx.author}", icon_url=ctx.author.avatar)
    await ctx.send(embed=info_embed)

@client.command()
async def say(ctx, *, text):
    await ctx.send(text)
    await ctx.message.delete()
    
 client.run('Discord Token')
