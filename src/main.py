import os
import random
import aiocron
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Initialize bot
load_dotenv()
bot = commands.Bot(command_prefix='pma ')


# Load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Couldn't put this in the Encouragement cog because of the way aiocron works
@aiocron.crontab('0 8 * * *')
async def daily_motivation():
    """Function that runs at 8am everyday and sends an embed to the default channel with some PMA message
    """
    morning_PMA = [
        'LET\'S GET THIS BREAD GAMERS LESSSSSSSSSSSSSSSSSSSSSSSSSSGOOOOOO',
        'Take a deep breath. You got this.',
        'The only thing you should doubt is your own self doubt. Go out there and make your mark.',
        'You are enough. You matter. You are visible. And you can make a difference.'
    ]
    e_dict = {
        'title': 'Daily Dose Of PMA',
        'description': random.choice(morning_PMA),
        'color': discord.Color.orange().value
    }
    # Temp_channel placeholder until I create the default channel functionality
    channel = bot.get_channel(int(os.getenv('TEMP_CHANNEL')))
    await channel.send(embed=discord.Embed.from_dict(e_dict))

bot.run(os.getenv('TOKEN'))
