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

#ban 
@client.command()
@has_permissions(administrator=True)
async def ban(ctx,user:discord.Member,reason="nincs indok"):
    await user.ban(reason=reason) 
    embed = discord.Embed(title=f"{user.name} ki lett bannolva {ctx.guild.name}, indok: {reason}",description=f"Bannolta {ctx.message.author}")
    await ctx.channel.send(embed = embed)
    await ctx.channel.send("https://c.tenor.com/Kt1irdU_daUAAAAC/ban-admin.gif")

@ban.error
async def ban_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}")
        await ctx.send(embed = embed)

#kick
@client.command()
@has_permissions(administrator=True)
async def kick(ctx,user:discord.Member,reason="nincs indok"):
    await user.kick(reason=reason) 
    embed = discord.Embed(title=f"{user.name} ki lett rúgva {ctx.guild.name}, indok: {reason}",description=f"Kirúgta {ctx.message.author}")
    await ctx.channel.send(embed = embed)

@kick.error
async def kick_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}")
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
             await ctx.channel.send(f"Unbanned: {user.mention}")

@unban.error
async def unban_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}")
        await ctx.send(embed = embed)



#ping
@client.command()
async def ping(ctx):
        embedVar = discord.Embed(title="Bot válaszideje")
        embedVar.add_field(name="Válaszidő", value=f'{round(client.latency * 1000)}ms', inline=False)
        await ctx.channel.send(embed=embedVar)

'''
#uptime
@client.command()
async def uptime(ctx):
    now = datetime.datetime.now()
    uptime = indulas - now
    uptime = datetime.timedelta.strftime(uptime, '%d nap %H óra %M perc %S másodperc')
    embedVar = discord.Embed(title="Bot futási ideje")
    embedVar.add_field(name="Idő", value = uptime, inline=False)
    await ctx.channel.send(embed=embedVar)'''



#avatar
@client.command(aliases=['av'])
async def avatar(ctx,user:discord.Member=None):
    if not user:
        user = ctx.message.author
    embed = discord.Embed()
    embed.set_image(url=user.avatar.url)
    embed.set_footer(text=f"Avatar from {user}")
    await ctx.channel.send(embed = embed)


'''#rangadó
@client.command()
@has_permissions(administrator=True)
async def rank(ctx, user: discord.Member, *, role: discord.Role ):
    await user.add_roles(role)
    await ctx.channel.send("A kért rangot sikeresen hozzá adtam az adott felhasználóhoz")

#rank hiba
async def rank_error(ctx,error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=f"Hiba",description=f"Nincs jogod ehhez {ctx.message.author.mention}")
        await ctx.send(embed = embed)'''
    
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
    
 client.run('Discord Token')
