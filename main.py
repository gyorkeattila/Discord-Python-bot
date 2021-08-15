from typing import AsyncIterator, DefaultDict
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.all() 
client = commands.Bot(command_prefix='=', intents = intents)


@client.event
async def on_ready():
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


#mlem
@client.command()
async def mlem(ctx):
    await ctx.channel.send("https://media.discordapp.net/attachments/861870461700014091/875830569894834186/20210813_215749.gif")



client.run('Discord Token')
