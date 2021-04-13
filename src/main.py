import os
import random
import discord
import aiocron
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
    e_dict = {
        'title': 'Here\'s Your Quote:',
        'description': quote,
        'color': discord.Color.orange().value
    }
    embed = discord.Embed.from_dict(e_dict)
    await ctx.trigger_typing()
    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount, check=purge_check)


@aiocron.crontab('0 8 * * *')
async def cronjob1():
    channel = bot.get_channel(830678928019554317)
    await channel.send('Good morning')


bot.run(os.getenv('TOKEN'))
