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

startTime = time.time()

if __name__ == '__main__':
    print("Tried to run {} as main script, despite it being a cog! Terminating script.".format(__file__))
    time.sleep(2)
    sys.exit()

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog loaded successfully.')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        """Classic magic 8ball command"""
        MagicBallPhrasesList = [
        "As I see it, yes.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Dont count on it.",
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
        "Yes, definitely.",
        "You may rely on it."]

        await ctx.send("Your question: {0}\nThe Magic 8ball's answer: {1}".format(question, MagicBallPhrasesList[random.randint(0,(len(MagicBallPhrasesList)) - 1)] + " {0}".format(ctx.message.author.mention)))
  
    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to give a question for the 8ball.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    async def coinflip(self, ctx):
        if random.randint(0, 1) == 0:
            await ctx.send("The result was heads!")
        else:
            await ctx.send("The result was tails!")

def setup(client):
    client.add_cog(Fun(client))