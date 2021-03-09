import discord
from discord.ext import commands
from functions import Game

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = open("TOKEN.txt", "r").read()
game = Game()


@Bot.event
async def on_ready():
    print("Hazırım")


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="gelen-gidenler")
    await channel.send(f"{member} Hoş Geldin Kanka")


@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="gelen-gidenler")
    await channel.send(f"@{member} Niye Gittin Mal Herif")


@Bot.command(aliases=["game", "oyun"])
async def egemen(ctx, *args):
    if "roll" in args:
        await ctx.send(game.roll_dice())
    else:
        await ctx.send("En iyisi!")


@Bot.command()
@commands.has_role("Admin")
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@Bot.command(aliases=["copy"])
async def clone_channel(ctx):
    await ctx.channel.clone()

@Bot.command()
@commands.has_role("Admin")
async def kick(ctx,member: discord.Member,*args,reason="Yok"):
    await member.kick(reason=reason)

@Bot.command()
@commands.has_role("Admin")
async def ban(ctx,member :discord.Member,*args,reason="Yok"):
    await member.ban(reason=reason)
@Bot.command()
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name,member_discriminator =member.split("#")
    for bans in banned_users:
        user = bans.user

        if(user.name,user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention}Kişisinin Banı Açıldı")
            return

Bot.run(TOKEN)
