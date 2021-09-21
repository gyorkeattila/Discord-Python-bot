from sqlite3.dbapi2 import Cursor
from typing import AsyncIterator, DefaultDict
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import sqlite3
import datetime


import ffmpeg
from discord import FFmpegPCMAudio

from discord import voice_client
from discord.utils import get



intents = discord.Intents.all() 
client = commands.Bot(command_prefix='=', intents = intents)


@client.event
async def on_ready():
    db = sqlite3.connect('bot.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warn(
        id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
        server_id TEXT, 
        user_id TEXT,
        amount INTEGER
        )
        ''')
    global indulas
    indulas = datetime.datetime.now()
    print('Szia Uram')

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

#spoderman
@client.command()
async def spoderman(ctx):
    await ctx.channel.send("https://media.discordapp.net/attachments/797151894275489802/875437827574366218/giphy.gif")

#peace
@client.command()
async def peace(ctx):
    await ctx.channel.send("https://c.tenor.com/DnY4rvDpLDwAAAAd/nileseyy-niles-disappear.gif")

#mlem
@client.command()
async def mlem(ctx):
    await ctx.channel.send("https://media.discordapp.net/attachments/861870461700014091/875830569894834186/20210813_215749.gif")

#warn
@client.command()
@has_permissions(administrator=True)
async def warn(ctx,member:discord.Member):
    db = sqlite3.connect('bot.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT amount FROM warn WHERE server_id = {ctx.guild.id} AND user_id = {member.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO warn (server_id, user_id, amount) VALUES (?, ?, ?)")
        val = (ctx.guild.id, member.id, '1')
        cursor.execute(sql, val)
        db.commit()
    elif result is not None:
        sql = ("INSERT INTO warn (server_id, user_id, amount) VALUES (?, ?, ?)")
        val = (ctx.guild.id, member.id, '1')
        cursor.execute(sql, val)
        db.commit()
    cursor.close()
    db.close()

#ping
@client.command()
async def ping(ctx):
        embedVar = discord.Embed(title="Bot válaszideje")
        embedVar.add_field(name="Válaszidő", value=f'{round(client.latency * 1000)}ms', inline=False)
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

#langos
@client.command()
async def langos(ctx):
    await ctx.channel.send("https://media.discordapp.net/attachments/754088236338642964/822194317257867334/image0-33.gif")


#zene
@client.command()
async def zene(ctx):
    user = ctx.author.voice
    if user is not None:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(executable="C:/Users/ati42/Desktop/ffmpeg-2021-09-01-git-c500dc7cca-full_build/bin/ffmpeg.exe", source=r"C:\Users\ati42\Desktop\Wenseron botja\friday.mp3"))
    else:
        await ctx.send("Nem vagy bent egy hangcsatornában sem")


#psg
@client.command()
async def psg(ctx):
    await ctx.channel.send("https://media.discordapp.net/attachments/670660610438070313/886837043890638848/received_4313099998758017.jpeg?width=654&height=676")

#avatar
@client.command(aliases=['av'])
async def avatar(ctx,user:discord.Member=None):
    if not user:
        user = ctx.message.author
    embed = discord.Embed()
    embed.set_image(url=user.avatar.url)
    embed.set_footer(text=f"Avatar from {user}")
    await ctx.channel.send(embed = embed)


client.run('Discord Token')
