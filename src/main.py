import os
import random
import aiocron
import discord
from dotenv import load_dotenv
from discord.ext import commands
from general_utils import parse_top3
from notion_utils import get_in_tray, get_todays_agenda, change_in_tray_title

# Initialize bot
load_dotenv()
bot = commands.Bot(command_prefix='pma ')


# Load all cogs
# Heroku specific path: /app/src/cogs
for filename in os.listdir('/app/src/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Couldn't put this in cogs because of the way aiocron works
@aiocron.crontab('0 2 * * *')
async def daily_report():
    """Function that runs at 7:30am everyday and sends an embed to the default channel with reports about pending tasks
    """
    morning_PMA = [
        'LET\'S GET THIS BREAD GAMERS LESSSSSSSSSSSSSSSSSSSSSSSSSSGOOOOOO',
        'Take a deep breath. You got this.',
        'The only thing you should doubt is your own self doubt. Go out there and make your mark.',
        'You are enough. You matter. You are visible. And you can make a difference.',
        'The only thing that matters is right now.'
    ]

    report = discord.Embed(
        title='Good Morning!',
        description=random.choice(morning_PMA),
        color=discord.Color.orange().value
    )
    # report.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    report.add_field(name='Here\'s your daily report',
                     value='Let\'s get some work done today!', inline=False)

    in_tray_pending = len(get_in_tray())
    todays_agenda = get_todays_agenda()

    if in_tray_pending > 0:
        report.add_field(name='Pending in tray item(s):',
                         value=f'{in_tray_pending}', inline=True)
    if len(todays_agenda) > 0:
        report.add_field(name='Item(s) on today\'s agenda:',
                         value=f'{len(todays_agenda)}', inline=True)
        top3_string = parse_top3(todays_agenda)
        report.add_field(name='Top item(s) on today\'s agenda:',
                         value=top3_string, inline=False)

    # Temp_channel placeholder until I create the default channel functionality
    channel = bot.get_channel(int(os.getenv('TEMP_CHANNEL')))
    await channel.send(embed=report)


@aiocron.crontab('0 */4 * * *')
async def in_tray_highlighter():
    """Function that runs every 4 hours to check if something is in the in tray and change the title accordingly
    """
    # TODO: Make the background of the in tray change when notion API lets you update blocks
    title = 'In tray'
    in_tray_elements = get_in_tray()
    if in_tray_elements is not None:
        title = f'In tray ({len(in_tray_elements)})'
    status_code = change_in_tray_title(title)
    # print(f"Action complete. Status code: {status_code}")

bot.run(os.getenv('TOKEN'))
