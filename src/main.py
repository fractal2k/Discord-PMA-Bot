import os
import random
import discord
from utils import get_quote
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
bot = commands.Bot(command_prefix='pma ')


def purge_check(msg):
    return (msg.author == bot.user) or (msg.content.startswith('pma '))


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(aliases=['hello', 'hey'])
async def hi(ctx):
    greetings = [
        'Hey!',
        'Hello',
        'Hi',
        'Hey there',
        'Yo',
        'Sup fam',
    ]
    await ctx.send(random.choice(greetings))


@bot.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)


@bot.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount, check=purge_check)


bot.run(os.getenv('TOKEN'))
