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
from googletrans import Translator
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
#       PRIORITY - Convert all commands to cogs
#
#       welcome - User can set a welcome message that the bot will dm to someone who joins the server
#       poll - Creates a poll that the server can vote on
#       img - Type a keyword or phrase and it googles the top result in google images.
#       help - Customise the help command 
#       joke - Tells a random joke from a database of jokes
#       Reactions - A range of commands that have a gif and an action e.g .slap would post a gif of someone getting slapped with '[user] was slapped by [user]!'.
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

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
    if not message.author.guild_permissions.manage_messages:
        with open('BannedWords.json', 'r') as f:
            bannedwords = json.load(f)
            for word in bannedwords[str(message.guild.id)]:
                if word in message.content.lower():
                    await message.delete()
                    print("Deleted message: '{}' in guild '{}' - {}".format(word, message.guild, datetime.datetime.now()))
            f.close()

    #   This allows the bot to listen to commands
    await bot.process_commands(message)

bot.run('XXX')
