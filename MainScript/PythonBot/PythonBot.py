#******************************************************/
#
#           Copyright (c) Harry Shepherd
#       I don't really care about copyright I
#       used this to make it feel like this code
#       is actually important. (hint: it ain't)
#
#******************************************************/
from discord.ext import commands
from threading import Timer
import asyncio
import json
import time
import datetime

bot = commands.Bot(command_prefix='.')

#                                       TODO:
#
#
#                                               - Continue work on the setreminder command.
#                                                   - Start with a time function
#                                                   - Send user DM on reminder

bannedWordList = []
reminderTime = ''

def clearBannedWordList():
    bannedWordList = []

def createBannedWordList():
    with open('BannedWords.txt', 'r') as fp:
        print("Opening BannedWords.txt in read mode")
        for cnt, line in enumerate(fp):
            tempLine = line.replace('\n', '')
            line = tempLine
            bannedWordList.append(line)
    fp.close()

createBannedWordList()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):

    #   Used in most commands to make sure the bot listens to the person who initiated the command.
    def check(m):
        return m and m.author == message.author


    #   Bans the naughty naughty words
    for word in bannedWordList:
        if word in message.content.lower():
            print("Deleted message '{0.content}' due to containing banned phrase.".format(message))
            await message.delete()

    #   Sends you the whole Shrek script line-by-line in your DM's. :)
    if message.content.startswith('.shrek'):
        user = bot.get_user(message.author.id)
        with open('ShrekScript.txt', 'r') as fp:
            for cnt, line in enumerate(fp):
                try:
                    await user.send(line)
                    print(line)
                    time.sleep(0.5)
                except:
                    pass
        fp.close()

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
            createBannedWordList()


bot.run('XXX')
