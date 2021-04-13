import os
import discord
from utils import get_quote
from discord.ext import commands


class Encouragement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        e_dict = {
            'title': 'Here\'s Your Quote:',
            'description': quote,
            'color': discord.Color.orange().value
        }
        embed = discord.Embed.from_dict(e_dict)
        await ctx.trigger_typing()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Encouragement(client))
