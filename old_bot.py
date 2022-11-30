import discord
from discord.ext import commands
import random
import praw
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import wolframalpha
from googletrans import Translator
import time

wolfClient = str(os.getenv('WOLF'))
client2 = wolframalpha.Client(wolfClient)
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Cool").sheet1
token = os.getenv('TOKEN')
client = commands.Bot(command_prefix = '_')
client.remove_command('help')
reddit = praw.Reddit("bot1", user_agent="Cyan's program 1.0 by /u/RosogollaBot")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('R.I.P Zyen'))
    print('bot is ready')


@client.command(aliases=['Ping'])
async def ping(ctx):
        embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

        embed.add_field(name='Ping', value=(f'```{round(client.latency * 1000)}ms```'), inline='False')
        await ctx.send(embed=embed)


@client.command(aliases=['8ball'])
async def eightoborru(ctx,* question):
    solved = ("")
    for x in question:
     solved += x
     solved += " "
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes – definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']

    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name='Question', value=(f'```{solved}```'), inline='False')
    embed.add_field(name='Answer', value=(f'```{random.choice(responses)}```'), inline='True')
    await ctx.send(embed=embed)


@client.command(aliases=['Clear'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    amount += 1
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name='Kicked Successfully', value=(f'Kicked {member.mention}'), inline='False')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)


    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name='Banned Successfully', value=(f'Banned {member.mention}'), inline='False')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user=None):

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Error: user could not be found!")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            await ctx.send("User not banned!")
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("Unbanning failed!")
        return

    await ctx.send(f"Successfully unbanned {user.mention}!")


@client.command(aliases=['red', 'Red', 'reddit'])
async def Reddit(ctx, sub: str):
    submision = reddit.subreddit(sub).hot()
    pick = random.randint(1,25)
    embed = discord.Embed(colour = discord.Colour(int("F8F8F8", 16)), description = f'{ctx.message.author.mention}')

    for i in range(0,pick):
        submission = next(x for x in submision if not x.stickied)

    percentUpvote = int(submission.upvote_ratio * 100)

    if submission.over_18 == True:
        embed.add_field(name="Error", value="Post is too lewd ><")
        await ctx.send(embed=embed)
    else:
        embed.set_author(name=submission.title, url=f'https://reddit.com/{submission.id}')
        embed.set_image(url=submission.url)
        embed.set_footer(text=f'{percentUpvote}% upvoted | {submission.score} upvotes')
        mesg = await ctx.send(embed=embed)
        await mesg.add_reaction("👍")
        await mesg.add_reaction("👎")


@client.event
async def on_command_error(ctx, message):
    embed = discord.Embed(
    colour= discord.Colour(int("F8F8F8", 16))
    )

    embed.add_field(name="Error", value=f'```{message}```')
    await ctx.send(embed=embed)


@client.command(aliases=['Say', 's', 'S'])
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


@client.command()
async def hug(ctx, member : discord.Member):
    hugsies = open("hugs.txt", "r")

    for line in hugsies:
        hugs = hugsies.readlines()

    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16)),
    description = f'{ctx.message.author.mention} hugs <@{member.id}>'
    )

    embed.set_image(url = random.choice(hugs))

    hugsies.close()

    await ctx.send(embed = embed)


@client.command()
async def pat(ctx, member : discord.Member):
    patsies = open("pats.txt", "r")

    for line in patsies:
        pats = patsies.readlines()

    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16)),
    description = f'{ctx.message.author.mention} hugs <@{member.id}>'
    )

    embed.set_image(url = random.choice(pats))

    patsies.close()

    await ctx.send(embed = embed)


@client.command()
async def commands(ctx):
    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.set_author(name='Commands')
    embed.add_field(name='Administration', value='`kick, ban, unban, clear`', inline = True)
    embed.add_field(name='Fun', value='`8ball, ping, say`', inline = True)
    embed.add_field(name='Imagery', value='`Reddit`', inline = True)
    embed.add_field(name='Interactions', value='`hug, pat`', inline = True)
    embed.add_field(name='Misc', value='`WolframAlpha, Schedule, Translate`', inline = True)

    await ctx.send(embed=embed)


@client.command(aliases = ["scd"])
async def Schedule(ctx, amt: int):
    embed = discord.Embed(
    colour = discord.Colour(int("F8F8F8", 16))
    )

    embed.set_author(name='2v2 Schedule')
    embed.add_field(name='ID', value=f'`{sheet.row_values(amt+1)[0]}`')
    embed.add_field(name='Team 1', value=f'`{sheet.row_values(amt+1)[3]}`')
    embed.add_field(name='Team 2', value=f'`{sheet.row_values(amt+1)[4]}`')
    embed.add_field(name='Date', value=f'`{sheet.row_values(amt+1)[1]}`')
    embed.add_field(name='Time', value=f'`{sheet.row_values(amt+1)[2]}`')

    await ctx.send(embed=embed)


@client.command(aliases = ['wa'])
async def WolframAlpha(ctx, query: str):
    res = client2.query(query)

    embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

    try:
        output = next(res.results).text
        embed.add_field(name='WolframAlpha', value=f'```{output}```')
        await ctx.send(embed=embed)

    except:
        embed.add_field(name='Error', value='Invalid Query')
        await ctx.send(embed=embed)


@client.command(aliases = ['t', 'translate'])
async def Translate(ctx, *, tex: str):
    translator = Translator()
    textt = tex.split()
    textv2 = " ".join(textt)

    translatedText = translator.translate([textv2])
    detectionstuff = translator.detect([textv2])
    embed = discord.Embed(
        colour = discord.Colour(int("F8F8F8", 16))
        )

    for translation in translatedText:
        embed.add_field(name="Original Text", value = f'```{textv2}```')
        embed.add_field(name="Translated Text", value = f'```{translation.text}```')
        for lang in detectionstuff:
            embed.set_footer(text=f"Translated from {lang.lang} to en")
    time.sleep(6)
    await ctx.send(embed=embed)

@client.command(aliases=["quit"])
async def close(ctx):
    if ctx.message.author.id == 426607245904838657:
        await client.close()
        print("Bot Closed")  # This is optional, but it is there to tell you.
    else:
        await ctx.send("you did a bruh moment")

client.run(token)
