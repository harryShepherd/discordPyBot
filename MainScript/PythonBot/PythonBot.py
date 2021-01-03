import discord
from discord.ext import commands
from discord.utils import get
from googletrans import Translator
from pyasn1.compat.octets import null
from threading import Timer
import datetime
import os
import json
import asyncio
import time
import random

#                                       TODO:
#
#   This is a list of commands that I plan to add to the bot in the future:
#
#       Test on_member_join method to see if it actually works
#
#
#       welcome - User can set a welcome message that the bot will dm to someone who joins the server
#       poll - Creates a poll that the server can vote on
#       img - Type a keyword or phrase and it googles the top result in google images.
#       help - Customise the help command
#       Reactions - A range of commands that have a gif and an action
#                   e.g .slap would post a gif of someone getting slapped with '[user] was slapped by [user]!'.
#       meirl - Gives a random top post from the me_irl subreddit
#       reddit - Gives a random post from a specified subreddit
#       subcount - Shows the subcount of a youtube channel
#       urban - Search urban dictonary
#       youtube - Searches youtube
#       osu - Show your osu stats

def getPrefix(bot, message):
    try:
        with open('Prefixes.json', 'r') as f:
            prefixes = json.load(f)
        f.close()
        return prefixes[str(message.guild.id)]
    except:
        # If this happens, then something has gone wrong with the server's prefix.
        # As a last ditch effort, it writes the server's prefix again.
        with open('Prefixes.json', 'r') as f:
            prefixes = json.load(f)
        f.close()
        prefixes[str(message.guild.id)] = '.'
        with open('Prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        f.close()
        print("Reset prefix for '{}' cause its corrupt or something idk - {}".format(message.guild, datetime.datetime.now()))


bot = commands.Bot(command_prefix=getPrefix)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


#   When the bot joins a new guild, it creates entries in the required json files
@bot.event
async def on_guild_join(guild):
    # Set up prefixes
    print("Joined guild: {}".format(guild))
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '.'
    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    f.close()

    # Set up banned words
    with open('BannedWords.json', 'r') as f:
        bannedWords = json.load(f)
    bannedWords[str(guild.id)] = []
    with open('BannedWords.json', 'w') as f:
        json.dump(bannedWords, f, indent=4)
    f.close()

    # Set up roles
    with open('Roles.json', 'r') as f:
        roles = json.load(f)
    roles[str(guild.id)] = {
        "Mute": null,
        "Gag": null,
        "OnJoin": null
    }
    with open('Roles.json', 'w') as f:
        json.dump(roles, f, indent=4)
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
async def on_member_join(member):
    with open('Roles.json', 'r') as f:
        roles = json.load(f)
    f.close()
    roleid = roles[str(member.server.id)]["OnJoin"]
    # Check to see if there is an OnJoin role
    if not roleid:
        pass
    else:
        await member.add_roles(get(member.server.roles, id=roleid))

@bot.event
async def on_message(message):
    #   Reads the user's message and detects if there is a banned word in it. If so, it deletes the message
    if not message.author.guild_permissions.manage_messages:
        with open('BannedWords.json', 'r') as f:
            bannedwords = json.load(f)
            for word in bannedwords[str(message.guild.id)]:
                if word in message.content.lower():
                    await message.delete()
                    print(
                        "Deleted message: '{}' in guild '{}' - {}".format(word, message.guild, datetime.datetime.now()))
            f.close()

    #   This allows the bot to listen to commands
    await bot.process_commands(message)


bot.run('XXX')
