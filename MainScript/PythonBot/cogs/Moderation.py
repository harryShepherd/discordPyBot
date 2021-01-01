import discord
from discord.ext import commands
from discord.utils import get
import datetime
import asyncio
import time
import json
import os
import sys

if __name__ == '__main__':
    print("Tried to run {} as main script, despite it being a cog! Terminating script.".format(__file__))
    time.sleep(2)
    sys.exit()

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation cog loaded successfully.')

    @commands.command()
    @commands.has_permissions(create_instant_invite=True)
    async def createinvite(self, ctx):
       """Creates an invite that lasts 5 minutes and send it to the chat"""
       link = await ctx.channel.create_invite(max_age = 300)
       await ctx.send("Here is an instant invite to your server: " + str(link))

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target: discord.Member, *, reason):
        """Kicks user that is tagged in the message"""
        await target.kick(reason=reason)
        await ctx.send("User {0} was kicked from the server.\nReason: {1}".format(target, reason))
        print("User '{}' was kicked from guild '{}' with reasion '{}' - {}".format(target, ctx.message.guild, reason, datetime.datetime.now()))

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("A reason is required.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("That user doesn't exist.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target: discord.Member, *, reason):
        """Bans user that is tagged in the message"""
        await target.ban(reason=reason)
        await ctx.send("User {0} was banned from the server.\nReason: {1}".format(target, reason))
        print("User '{}' was banned from guild '{}' with reasion '{}' - {}".format(target, ctx.message.guild, reason, datetime.datetime.now()))


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("A reason is required.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("That user doesn't exist.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        """Deletes x amount of messages from the channel the user uses this command in"""
        amount = await ctx.channel.purge(limit=limit)
        await ctx.send("Deleted {} messsages".format(len(amount)))
        print("Purged {} messages in guild '{}' - {}".format(limit, ctx.message.guild, datetime.datetime.now()))

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify how many messages you want me to purge.")

    @commands.command()
    async def prefix(self, ctx, prefix: str):
        """Changes the prefix for the specified server"""
        with open(os.path.join(os.getcwd(), 'Prefixes.json'), 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open(os.path.join(os.getcwd(), 'Prefixes.json'), 'w') as f:
            json.dump(prefixes, f, indent=4)
        f.close()
        await ctx.send("Changed server prefix to `{}`.".format(prefix))
        print("Changed prefix to: '{}' in guild '{}' - {}".format(prefix, ctx.message.guild, datetime.datetime.now()))

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            prefix = ""
            with open(os.path.join(os.getcwd(), 'Prefixes.json'), 'r') as f:
                prefixes = json.load(f)
            prefix = prefixes[str(ctx.guild.id)]
            await ctx.send("The prefix for this server is `{}`".format(prefix))
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def banword(self, ctx, word):
        """Allows the user to add a word to the ban list for the server"""
        print("Banned word: '{}' in guild '{}' - {}".format(word, ctx.message.guild, datetime.datetime.now()))
        with open(os.path.join(os.getcwd(), 'BannedWords.json'),'r') as f:
            bannedwords = json.load(f)
        bannedwords[str(ctx.guild.id)].append(word.lower())
        with open(os.path.join(os.getcwd(), 'BannedWords.json') ,'w') as f:
            json.dump(bannedwords, f, indent=4)
        f.close()
        await ctx.send("I've banned the word.")

    @banword.error
    async def banword_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to say a word to ban.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have the permissions to do that.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unbanword(self, ctx, word: str):
        """Allows the user to remove a word from the ban list for the server"""
        with open(os.path.join(os.getcwd(), 'BannedWords.json'), 'r') as f:
            banwords = json.load(f)
            banwords[str(ctx.guild.id)].remove(word.lower())
        f.close()
        with open(os.path.join(os.getcwd(), 'BannedWords.json'), 'w') as f:
            json.dump(banwords, f, indent=4)
        f.close()
        await ctx.send("Unbanned the word {}.".format(word.lower()))

    @unbanword.error
    async def unbanword_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to say a word to unban.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have the permissions to do that.")
        else:
            await ctx.send("Something went wrong.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setmuterole(self, ctx, role: discord.Role):
        """Allows the user to select a role which will be used for muting other users"""
        with open('Roles.json', 'r') as f:
            roles = json.load(f)
        f.close()
        roles[str(ctx.guild.id)]["Mute"] = role.id
        with open('Roles.json', 'w') as f:
            json.dump(roles, f, indent=4)
        f.close()

    @setmuterole.error
    async def setmuterole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a role.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have permissions to do that.")
        else:
            await ctx.send("Something went wrong")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, target: discord.Member, duration):
        """Mutes a specified user for a duration"""
        with open('Roles.json', 'r') as f:
            roles = json.load(f)
        f.close()
        roleid = roles[str(ctx.guild.id)]["Mute"]
        print(roleid)
        await target.add_roles(get(ctx.guild.roles, id=roleid))
        await asyncio.sleep(int(duration))
        await target.remove_roles(get(ctx.guild.roles, id=roleid))

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot to include a user and/or duration.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have permissions to do that.")
        else:
            await ctx.send("Something went wrong")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, target: discord.Member):
        """Unmutes a specified user"""
        with open('Roles.json', 'r') as f:
            roles = json.load(f)
        f.close()
        roleid = roles[str(ctx.guild.id)]["Mute"]
        await target.remove_roles(get(ctx.guild.roles, id=roleid))

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot to include a user.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have permissions to do that.")
        else:
            await ctx.send("Something went wrong")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setgagrole(self, ctx, role: discord.Role):
        """Allows the user to select a role which will be used for muting other users"""
        with open('Roles.json', 'r') as f:
            roles = json.load(f)
        f.close()
        roles[str(ctx.guild.id)]["Gag"] = role.id
        with open('Roles.json', 'w') as f:
            json.dump(roles, f, indent=4)
        f.close()

    @setgagrole.error
    async def setgagrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a role.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have permissions to do that.")
        else:
            await ctx.send("Something went wrong")
            print(error)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def gag(self, ctx, target: discord.Member, duration):
        """Mutes a specified user for a duration"""
        with open('Roles.json', 'r') as f:
            roles = json.load(f)
        f.close()
        roleid = roles[str(ctx.guild.id)]["Gag"]
        print(roleid)
        await target.add_roles(get(ctx.guild.roles, id=roleid))
        await asyncio.sleep(int(duration))
        await target.remove_roles(get(ctx.guild.roles, id=roleid))

    @gag.error
    async def gag_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot to include a user and/or duration.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have permissions to do that.")
        else:
            await ctx.send("Something went wrong")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def ungag(self, ctx, target: discord.Member):
        """Unmutes a specified user"""
        with open('Roles.json', 'r') as f:
            roles = json.load(f)
        f.close()
        roleid = roles[str(ctx.guild.id)]["Gag"]
        await target.remove_roles(get(ctx.guild.roles, id=roleid))

    @ungag.error
    async def ungag_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot to include a user.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have permissions to do that.")
        else:
            await ctx.send("Something went wrong")

def setup(client):
    client.add_cog(Moderation(client))