import discord
from discord.ext import commands
import datetime
import time
import os
import sys

startTime = time.time()

if __name__ == '__main__':
    print("Tried to run {} as main script, despite it being a cog! Terminating script.".format(__file__))
    time.sleep(2)
    sys.exit()

class Utilities(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog loaded successfully.')

    @commands.command()
    async def en(self, ctx, *translation):
        """Translates text to English"""
        translator = Translator()
        translation = translator.translate((' '.join(translation)), dest='en')
        embed=discord.Embed(title='', color=0x0b6a39)
        embed.add_field(name='Translation', value=translation.text, inline=False)
        footertext = '{} -> {}'.format(translation.src, translation.dest)
        embed.set_footer(text=footertext)
        await ctx.send(embed=embed)

    @en.error
    async def en_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please provide text to translate.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    async def fr(self, ctx, *translation):
        """Translates text to French"""
        translator = Translator()
        translation = translator.translate((' '.join(translation)), dest='fr')
        embed=discord.Embed(title='Translation', color=0x0b6a39)
        embed.add_field(name='{} -> {}'.format(translation.src, translation.dest), value=translation.text, inline=False)
        await ctx.send(embed=embed)

    @fr.error
    async def fr_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please provide text to translate.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    async def ja(self, ctx, *translation):
        """Translates text to Japanese"""
        translator = Translator()
        translation = translator.translate((' '.join(translation)), dest='ja')
        embed=discord.Embed(title='Translation', color=0x0b6a39)
        embed.add_field(name='{} -> {}'.format(translation.src, translation.dest), value=translation.text, inline=False)
        await ctx.send(embed=embed)

    @ja.error
    async def ja_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please provide text to translate.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    async def suggestion(ctx, *suggestion):
        """Do you have an idea that can improve the bot? Leave a suggestion!"""
        print(suggestion)
        with open('Suggestions.json', 'r') as f:
            suggestionJson = json.load(f)
        suggestionJson.append(' '.join(suggestion))
        with open('Suggestions.json', 'w') as f:
            json.dump(suggestionJson, f, indent=4)
        f.close()

def setup(client):
    client.add_cog(Utilities(client))