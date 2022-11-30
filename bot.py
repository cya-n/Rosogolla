import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.all()
intents.message_content = True
token = str(os.getenv('TOKEN'))
client = commands.Bot(command_prefix = "_", intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('how'))
    print('bot is ready')

@client.command(aliases=['Ping'])
async def ping(ctx):
        embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

        embed.add_field(name='Ping', value=(f'```{round(client.latency * 1000)}ms```'), inline='False')
        await ctx.send(embed=embed)



@client.command(aliases=["XP"])
async def xp(ctx, *, member: discord.Member = None):
    f = open('levels.json', encoding="utf8")
    data = json.load(f)
    for i in range(len(data)):
        if str(ctx.message.author.id) == data[i]["id"]:
            embed = discord.Embed(
                colour = discord.Colour(int("F8F8F8", 16)),                
            )
            percentage = int((data[i]["detailed_xp"][0])/(data[i]["detailed_xp"][1])*100)
            embed.add_field(name="Username", value=f'```{data[i]["username"]}#{data[i]["discriminator"]}```')
            embed.add_field(name="Level",value=f'```{data[i]["level"]}```')
            embed.add_field(name="Percentage", value=f'```{percentage}%```')
            if not member:
                member = ctx.message.author
            avatar = member.avatar.url
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="Progress Bar", value=(("🟩"*round(percentage/10)) + "🟨"*(10-round(percentage/10))))
            await ctx.send(embed = embed)
    f.close()

@client.command(aliases=["quit"])
async def close(ctx):
    if ctx.message.author.id == 426607245904838657:
        await client.close()
        print("Bot Closed")
    else:
        await ctx.send("you did a bruh moment")

@client.event
async def on_command_error(ctx, message):
    embed = discord.Embed(
    colour= discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name="Error", value=f'```{message}```')
    await ctx.send(embed=embed)

client.run(token)
