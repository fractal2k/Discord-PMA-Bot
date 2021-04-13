import discord
import random
from discord.ext import commands


class Base(commands.Cog):
    """Cog containing base bot functionality"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Prints a ready message in the terminal once the bot is ready for operations"""
        print(f'{self.client.user} is ready')

    @commands.command(aliases=['hello', 'hey'])
    async def hi(self, ctx):
        """Greets the user by pulling a random greeting from a list of different greeting messages"""
        greetings = [
            'Hey!',
            'Hello',
            'Hi',
            'Hey there',
            'Yo',
            'Sup fam',
        ]
        await ctx.send(random.choice(greetings))

    @commands.command()
    async def clear(self, ctx, amount=10):
        """Clears the specified (or default if not) amount of bot related messages 
        from the channel the command is called in"""
        await ctx.channel.purge(limit=amount, check=self.purge_check)

    def purge_check(self, msg):
        """Custom function to check if the message is bot related"""
        return (msg.author == self.client.user) or (msg.content.startswith('pma '))


def setup(client):
    client.add_cog(Base(client))
