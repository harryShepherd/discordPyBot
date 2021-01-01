import discord
from tweepy import OAuthHandler
from tweepy import API
from discord.ext import commands
import datetime
import time
import os
import sys

startTime = time.time()

""" Tweepy Setup """
consumer_key = "XXX"
consumer_secret = "XXX"
access_token = "XXX"
access_token_secret = "XXX"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)
""""#############"""


if __name__ == '__main__':
    print("Tried to run {} as main script, despite it being a cog! Terminating script.".format(__file__))
    time.sleep(2)
    sys.exit()

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Info cog loaded successfully.')

    @commands.command()
    async def avatar(self, ctx, *, avamember : discord.Member=None):
        """Sends the tagged user's avatar"""
        userAvatarUrl = avamember.avatar_url
        await ctx.send(userAvatarUrl)

    @avatar.error
    async def avatar_error(self, ctx, error):
        await ctx.send("That user is invalid.")

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        """Shows information about a given user"""
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
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a user.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that user.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    async def botinfo(self, ctx):   
        """Shows information about the bot"""
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
    async def botinfo_error(self, ctx, error):
        await ctx.send("Something went wrong.")

    @commands.command()
    async def serverinfo(self, ctx):
        """Shows information about the server the user is in"""
        embed=discord.Embed(title=None, color=0x1aa018)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Guild Info', value='**Created On**: {}\n**Owner**: {}\n**Members**: {}\n**Channels**: {}\n**Region**: {}\n**Verification Level**: {}'.format(ctx.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), ctx.guild.owner, ctx.guild.member_count, len(ctx.guild.voice_channels) + len(ctx.guild.text_channels), str(ctx.guild.region).capitalize(), str(ctx.guild.verification_level).capitalize()), inline=True)   
        await ctx.send(embed=embed)

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        await ctx.send("Something went wrong.")

    @commands.command()
    async def twitterinfo(selfself, ctx, target):
        """Shows information about a twitter user"""
        item = auth_api.get_user(target)
        embed=discord.Embed(title=None, color=0x1aa018)
        embed.set_thumbnail(url=item.profile_image_url)
        embed.add_field(name=target + "'s info", value="**Name**: {}\n**Tag**: {}\n**Bio**: {}\n**Statuses Count**: {}\n**Following Count**: {}\n**Followers Count**: {}".format(item.name, item.screen_name, item.description, str(item.statuses_count), str(item.friends_count), str(item.followers_count)))
        await ctx.send(embed=embed)

    @twitterinfo.error
    async def twitterinfo_error(self, ctx, error):
        await ctx.send("Something went wrong. Check that the user you specified exists.")

def setup(client):
    client.add_cog(Info(client))