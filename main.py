from sqlite3.dbapi2 import Cursor
from typing import AsyncIterator, DefaultDict
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import sqlite3

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



client.run('Discord Token')
