#******************************************************/
#
#           Copyright (c) Harry Shepherd
#       I don't really care about copyright I
#       used this to make it feel like this code
#       is actually important. (hint: it ain't)
#
#******************************************************/
import discord
from discord.ext import commands
from threading import Timer
import json
import asyncio
import time
import random
#                                       TODO:   
#
#   This is a list of commands that I plan to add to the bot in the future:
#
#       coinflip - Flips a coin
#       img - Type a keyword or phrase and it googles the top result in google images.
#       Reactions - A range of commands that have a gif and an action e.g .slap would post a gif of someone getting slapped with '[user] was slapped by [user]!'.
#       info - Gets information abouts the bot and spurts it out
#       autorole - Set if you want to set a role to people when they join your server
#       gag - Prevents a user from typing in any channel for x amount of seconds
#       mute - Mutes and unmutes mentioned user
#       meirl - Gives a random top post from the me_irl subreddit
#       subcount - Shows the subcount of a youtube channel
#       urban - Search urban dictonary
#       youtube - Searches youtube
#       osu - Show your osu stats

bannedWordList = []
def createBannedWordList():
    with open('BannedWords.txt', 'r') as fp:
        for cnt, line in enumerate(fp):
            tempLine = line.replace('\n', '')
            line = tempLine
            bannedWordList.append(line)
    fp.close()
createBannedWordList()

def getPrefix(bot, message):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=getPrefix)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_guild_join(guild):
    print("Joined guild: {}".format(guild))
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '.'
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    print("Left guild: {}".format(guild))
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_message(message):

    #   Used in most commands to make sure the bot listens to the person who initiated the command
    def check(m):
        return m and m.author == message.author


    #   Deletes any messages containing banned words
    for word in bannedWordList:
        if word in message.content.lower():
            print("Deleted message '{0.content}' due to containing banned phrase.".format(message))
            await message.delete()

    #   Adds words to naughty list 
    #   This took so much longer than it needed to...
    if message.content.startswith('.banword'):
        await message.channel.send("What word are you banning {0.author.mention}?".format(message))
        try:
            chosenWord = await bot.wait_for('message', check=check, timeout = 10.0)
        except asyncio.TimeoutError:
            await message.channel.send("Took too long idiot")
        else:
            with open('BannedWords.txt', 'a+') as fp:
                fp.write("\n{0}".format(chosenWord.content))
            fp.close()
            await message.channel.send("Added {0} to the list of banned words.".format(chosenWord.content))
            BannedWordList = []
    #   This allows the bot to listen to commands
    await bot.process_commands(message)

#   Sends the tagged user's avatar
@bot.command()
async def avatar(ctx, *, avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@avatar.error
async def avatar_error(ctx, error):
    await ctx.send("That user is invalid")


#   Classic magic 8ball command
@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    MagicBallPhrasesList = [
    "As I see it, yes.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don’t count on it.",
    "It is certain.",
    "It is decidedly so.",
    "Most likely.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Outlook good.",
    "Reply hazy, try again.",
    "Signs point to yes.",
    "Very doubtful.",
    "Without a doubt.",
    "Yes.",
    "Yes – definitely.",
    "You may rely on it."]

    await ctx.send("Your question: {0}\nThe Magic 8ball's answer: {1}".format(question, MagicBallPhrasesList[random.randint(0,(len(MagicBallPhrasesList)) - 1)] + " {0}".format(ctx.message.author.mention)))
  
@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to give a question for the 8ball")
    else:
        await ctx.send("Something went wrong")

#   Creates an invite that lasts 5 minutes and send it to the chat
@bot.command()
async def createinvite(ctx):
       link = await message.channel.create_invite(max_age = 300)
       await ctx.send("Here is an instant invite to your server: " + str(link))

#   Responds with the latency time of the bot
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(bot.latency, 3)))

#   Kicks user that is tagged in the message
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, target: discord.Member, *, reason):
    await target.kick(reason=reason)
    await ctx.send("User {0} was kicked from the server.\nReason: {1}".format(target, reason))

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A reason is required.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("That user doesn't exist.")

#   Bans user that is tagged in the message
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, target: discord.Member, *, reason):
    await target.ban(reason=reason)
    await ctx.send("User {0} was banned from the server.\nReason: {1}".format(target, reason))

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A reason is required.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("That user doesn't exist.")

#   Deletes x amount of messages from the channel the user uses this command in
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    amount = await ctx.channel.purge(limit=limit)
    await ctx.send("Deleted {} messsages".format(len(amount)))

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify how many messages you want me to purge.")

@bot.command()
async def prefix(ctx, prefix):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send("Changed server prefix to {}.".format(prefix))

bot.run('XXX')
