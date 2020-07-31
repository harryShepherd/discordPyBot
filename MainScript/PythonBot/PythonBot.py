#******************************************************/
#
#           Copyright (c) Harry Shepherd
#       I don't really care about copyright I
#       used this to make it feel like this code
#       is actually important. (hint: it ain't)
#
#******************************************************/
import discord
from threading import Timer
import asyncio
import time
import random

bot = discord.Client()

#                                       TODO:
#
#   This is a list of commands that I plan to add to the bot in the future:
#
#       8ball - Gives random response like a magic 8ball                                    [x]
#       autorole - Set if you want to set a role to people when they join your server       []
#       avatar - Shows you your Avatar                                                      []
#       ban - Bans mentioned user                                                           []
#       help - Displays all the available commands for your permission level                []
#       insult - Gives you a random insult                                                  []
#       invite - Create an invite for the server                                            []
#       kick - Kicks mentioned user                                                         []
#       mute - Mutes and unmutes mentioned user                                             []
#       ping - Ping/Pong command. I wonder what this does? /sarcasm                         []
#       prefix - Change the prefix for your server                                          []
#       purge - Purges X amount of messages from a given channel                            []
#       quote - Random famous quote                                                         []
#       subcount - Shows the subcount of a youtuber                                         []
#       urban - Search urban dictonary                                                      []
#       youtube - Searches youtube                                                          []
#       osu - Show your osu stats                                                           []



#   List of pre-defined variables
bannedWordList = []
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
    print('Logged in as {0.user}'.format(bot))
    print("I'm in " + str(len(bot.guilds)) + ' servers:')
    for server in bot.guilds:
        print('    ' + str(server))

@bot.event
async def on_message(message):

    #   Used in most commands to make sure the bot listens to the person who initiated the command.
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

    #   A classic 8ball command
    if message.content.startswith('.8ball'):
        await message.channel.send('What is your query for the magic 8ball?')       
        try:
            await bot.wait_for('message', check=check, timeout = 10.0)
        except asyncio.TimeoutError:
            await message.channel.send('You took too long to respond.')
        else:
            await message.channel.send(MagicBallPhrasesList[random.randint(0,(len(MagicBallPhrasesList)) - 1)] + " {0}".format(message.author.mention))


bot.run('XXX')
