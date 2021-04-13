import discord
import random
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.client.user} is ready')

    @commands.command(aliases=['hello', 'hey'])
    async def hi(self, ctx):
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
        await ctx.channel.purge(limit=amount, check=self.purge_check)

    def purge_check(self, msg):
        return (msg.author == self.client.user) or (msg.content.startswith('pma '))


def setup(client):
    client.add_cog(Base(client))
