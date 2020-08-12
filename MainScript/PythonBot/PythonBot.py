#******************************************************/
#
#           Copyright (c) Harry Shepherd
#       I don't really care about copyright I
#       used this to make it feel like this code
#               is actually important.
#
#******************************************************/
import discord
from discord.ext import commands
from threading import Timer
import json
import asyncio
import time
import random

startTime = time.time()
#                                       TODO:   
#
#   This is a list of commands that I plan to add to the bot in the future:
#
#       coinflip - Flips a coin
#       welcome - User can set a welcome message that the bot will dm to someone who joins the server
#       poll - Creates a poll that the server can vote on
#       img - Type a keyword or phrase and it googles the top result in google images.
#       help - Customise the help command 
#       joke - Tells a random joke from a database of jokes
#       Reactions - A range of commands that have a gif and an action e.g .slap would post a gif of someone getting slapped with '[user] was slapped by [user]!'.
#       botinfo - Gets information abouts the bot and spurts it out
#       serverinfo - Gets information about the server
#       autorole - Set if you want to set a role to people when they join your server
#       gag - Prevents a user from typing in any channel for x amount of seconds
#       mute - Mutes and unmutes mentioned user
#       ungag - Ungags a user
#       unmute - Unmutes a user
#       unban - Unbans a user
#       meirl - Gives a random top post from the me_irl subreddit
#       reddit - Gives a random post from a specified subreddit
#       aimeme - Creates a meme using ai | Not currently possible through api.
#       subcount - Shows the subcount of a youtube channel
#       urban - Search urban dictonary
#       youtube - Searches youtube
#       osu - Show your osu stats

def getPrefix(bot, message):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=getPrefix)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

#   When the bot joins a new guild, it creates entries in the required json files
@bot.event
async def on_guild_join(guild):
    print("Joined guild: {}".format(guild))
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '.'
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    f.close()

    with open('BannedWords.json', 'r') as f:
        bannedWords = json.load(f)
    bannedWords[str(guild.id)] = []
    with open('BannedWords.json', 'w') as f:
        json.dump(bannedWords, f, indent=4)
    f.close()

#   When the bot is removed from a guild, it removes the entries it has in the json files
@bot.event
async def on_guild_remove(guild):
    print("Left guild: {}".format(guild))
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    f.close()

    with open('BannedWords.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('BannedWords.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    f.close()

@bot.event
async def on_message(message):
    #   Reads the user's message and detects if there is a banned word in it. If so, it deletes the message
    if not message.author.guild_permissions.administrator:
        with open('BannedWords.json', 'r') as f:
            bannedwords = json.load(f)
            for word in bannedwords[str(message.guild.id)]:
                if word in message.content.lower():
                    await message.delete()
            f.close()

    #   This allows the bot to listen to commands
    await bot.process_commands(message)

#   Sends the tagged user's avatar
@bot.command()
async def avatar(ctx, *, avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@avatar.error
async def avatar_error(ctx, error):
    await ctx.send("That user is invalid.")

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
        await ctx.send("You need to give a question for the 8ball.")
    else:
        await ctx.send("Something went wrong.")

#   Creates an invite that lasts 5 minutes and send it to the chat
@bot.command()
#@commands.has_permissions(create_invite=True)
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

#   Changes the prefix for the specified server
@bot.command()
async def prefix(ctx, prefix):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    f.close()
    await ctx.send("Changed server prefix to {}.".format(prefix))

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify a prefix to set.")
    else:
        await ctx.send("Something went wrong.")

#   Allows the user to add a word to the ban list for the server
@bot.command()
@commands.has_permissions(manage_messages=True)
async def banword(ctx, word):
    with open('BannedWords.json','r') as f:
        bannedwords = json.load(f)
    bannedwords[str(ctx.guild.id)].append(word.lower())
    with open('BannedWords.json' ,'w') as f:
        json.dump(bannedwords, f, indent=4)
    f.close()
    await ctx.send("I've banned the word.")


@banword.error
async def banword_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to say a word to ban.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the permissions to do that.")
    else:
        await ctx.send("Something went wrong.")

#   Allows the user to remove a word from the ban list for the server
@bot.command()
@commands.has_permissions(manage_messages=True)
async def unbanword(ctx, word: str):
    with open('BannedWords.json', 'r') as f:
        banwords = json.load(f)
        banwords[str(ctx.guild.id)].remove(word.lower())
    f.close()
    with open('BannedWords.json', 'w') as f:
        json.dump(banwords, f, indent=4)
    f.close()
    await ctx.send("Unbanned the word {}.".format(word.lower()))

@unbanword.error
async def unbanword_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to say a word to unban.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the permissions to do that.")
    else:
        await ctx.send("Something went wrong.")

#   Shows information about a given user
@bot.command()
async def userinfo(ctx, user: discord.Member):
    embed=discord.Embed(title=user.nick, color=0x1aa018)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name='Member Information', value='**Display Name**: {}\n**Joined At**: {}\n**Roles**: {}'.format(user.display_name, user.joined_at, user.top_role), inline=False)
    embed.add_field(name='User Information', value='**ID**: {}\n**Username**: {}\n**Discriminator**: {}\n**Created At**: {}'.format(user.id, user.name, user.discriminator, user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")), inline=False)
    #   The currently playing part would say 'None' if a user isn't playing anything with sounds off, so I changed it to say 'Nothing'
    if str(user.activity) == "None":
        embed.add_field(name='**Currently Playing**', value='Nothing', inline=False)
    else:
        embed.add_field(name='**Currently Playing**', value=user.activity, inline=False)
    await ctx.send(embed=embed)

@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify a user.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Could not find that user.")
    else:
        await ctx.send("Something went wrong.")

#   Shows information about the bot
@bot.command()
async def botinfo(ctx):   
    s = time.time() - startTime
    d = int(s / 60 / 60 / 24 % 365)
    h = int(s / 60 / 60 % 24)   
    m =int(s / 60 % 60)    
    sec = int(s % 60) 
    embed=discord.Embed(title=None, color=0x1aa018)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name='Bot Info', value='**Bot Name**: {}\n**Servers**: {}\n**Channels**: {}\n**Created On**: {}\n**Uptime**: {} d {} h {} m {} s'.format(bot.user.name, len(bot.guilds), len(ctx.message.guild.text_channels + ctx.message.guild.voice_channels), bot.user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), d, h, m, sec), inline=True)   
    await ctx.send(embed=embed)

@botinfo.error
async def botinfo_error(ctx, error):
    await ctx.send("Something went wrong.")
    await ctx.send(error)

#   Shows information about the server the user is in
@bot.command()
async def serverinfo(ctx):
    embed=discord.Embed(title=None, color=0x1aa018)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name='Guild Info', value='**Created On**: {}\n**Owner**: {}\n**Members**: {}\n**Channels**: {}\n**Region**: {}\n**Verification Level**: {}'.format(ctx.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), ctx.guild.owner, ctx.guild.member_count, len(ctx.guild.voice_channels) + len(ctx.guild.text_channels), str(ctx.guild.region).capitalize(), str(ctx.guild.verification_level).capitalize()), inline=True)   
    await ctx.send(embed=embed)

@serverinfo.error
async def serverinfo_error(ctx, error):
    await ctx.send("Something went wrong.")
    await ctx.send(error)

bot.run('XXX')
