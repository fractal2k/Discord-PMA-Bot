import os
import discord
import aiocron
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
bot = commands.Bot(command_prefix='pma ')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@aiocron.crontab('0 8 * * *')
async def cronjob1():
    channel = bot.get_channel(int(os.getenv('TEMP_CHANNEL')))
    await channel.send('Good morning')

bot.run(os.getenv('TOKEN'))
