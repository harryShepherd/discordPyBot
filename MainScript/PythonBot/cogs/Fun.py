import discord
from discord.ext import commands
import praw
from threading import Timer
import datetime
import json
import asyncio
import requests
import time
import random
import os
import sys

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

    @commands.command()
    async def dadjoke(self, ctx):
        """Sends a funny dad joke"""
        url = "https://dad-jokes.p.rapidapi.com/random/joke"
        headers = {
            'x-rapidapi-key': "XXX",
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers)
        parsed_response = json.loads(response.text)
        await ctx.send(parsed_response["body"][0]["setup"])
        await asyncio.sleep(1)
        await ctx.send(parsed_response["body"][0]["punchline"])


def setup(client):
    client.add_cog(Fun(client))