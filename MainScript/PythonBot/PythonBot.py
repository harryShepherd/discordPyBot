#******************************************************/
#
#           Copyright (c) Harry Shepherd
#       I don't really care about copyright I
#       used this to make it feel like this code
#       is actually important. (hint: it ain't)
#
#******************************************************/
from discord.ext import commands
import asyncio
import json
import datetime

#   Don't touch. Magic stuff.
bot = commands.Bot(command_prefix='.')

#                                       TODO:
#
#
#                                               - Continue work on the setreminder command.
#                                                   - Send user DM on reminder

bannedWordList = []

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


    #   Bans the naughty naughty words >:)))
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
            createBannedWordList()

    if message.content.startswith('.test'):
        await message.channel.send('Test')

    if message.content.startswith('.setreminder'):
        date = ""
        reminder = ""
        await message.channel.send("On what day would you like to set this reminder {0.author.mention}?".format(message))
        try:
            chosenDate = await bot.wait_for('message', check=check, timeout = 10.0)
        except asyncio.TimeoutError:
            await message.channel.send("Took too long idiot")
        else:
            await message.channel.send("You said {0}".format(chosenDate.content))

            if(int(chosenDate.content) < int(datetime.date.day)):
                chosenMonth = int(datetime.date.month) + 1
                if(chosenMonth == 1):
                    chosenYear = int(datetime.date.year) + 1
                else:
                    chosenYear = int(datetime.date.year)
            print(str(chosenYear) + str(chosenMonth) + chosenDate.content)

#@bot.command()
#async def setreminder(ctx):
#    date = ""
#    reminder = ""
#    await ctx.channel.send("On what day would you like to set this reminder {0.author.mention}?".format(ctx.message))
#    chosenDate = bot.wait_for('message', check = False, timeout = 10.0)
#    await ctx.channel.send("What time would you like to be reminded {0.author.mention}?".format(ctx.message))
#    chosenTime = bot.wait_for('message', check = False, timeout = 10.0)
#    await ctx.channel.send("And what would you like to be reminded about {0.author.mention}?".format(ctx.message))
#    TempReminder = bot.wait_for('message', check = False, timeout = 10.0)
#    reminder = TempReminder.content()
#    await ctx.channel.send("So you want me to set a reminder for {0} at {1} for '{2}'?".format(chosenDate, chosenTime, reminder))


bot.run('XXX')
