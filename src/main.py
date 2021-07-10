import os
import random
import aiocron
import discord
from dotenv import load_dotenv
from discord.ext import commands
from notion import InTray, TodaysAgenda, WaitingList

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
    intray = InTray()
    tagenda = TodaysAgenda()
    wlist = WaitingList()

    report = discord.Embed(
        title='Good Morning!',
        description=random.choice(morning_PMA),
        color=discord.Color.orange().value
    )
    # report.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    report.add_field(name='Here\'s your daily report',
                     value='Let\'s get some work done today!', inline=False)

    in_tray_pending = len(intray.get_tray())
    todays_agenda = tagenda.get_agenda()
    waiting = wlist.get_list()

    if in_tray_pending > 0:
        report.add_field(name='Pending in tray item(s):',
                         value=f'{in_tray_pending}', inline=True)
    if len(todays_agenda) > 0:
        report.add_field(name='Item(s) on today\'s agenda:',
                         value=f'{len(todays_agenda)}', inline=True)
        top3_string = '\n'.join(
            [f'{idx}. {item}' for idx, item in enumerate(todays_agenda[:3], 1)])
        report.add_field(name='Top item(s) on today\'s agenda:',
                         value=top3_string, inline=False)
    if len(waiting) > 0:
        report.add_field(name='Item(s) in waiting list:',
                         value=f'{len(waiting)}', inline=True)

    # Temp_channel placeholder until I create the default channel functionality
    channel = bot.get_channel(int(os.getenv('TEMP_CHANNEL')))
    await channel.send(embed=report)


@aiocron.crontab('0 */4 * * *')
async def page_highlighter():
    """Function that runs every 4 hours to check if something is in the in tray and waiting list and changes the title accordingly
    """
    # TODO: Make the background of the in tray change when notion API lets you update blocks
    intray = InTray()
    wlist = WaitingList()
    tray = intray.get_tray()
    waiting = wlist.get_list()
    tray_title = 'In tray'
    wlist_title = 'Waiting'

    if len(tray) > 0:
        tray_title = f'In tray ({len(tray)})'
    if len(waiting) > 0:
        wlist_title = f'Waiting ({len(waiting)})'

    status_code = intray.change_title(new_title=tray_title)
    status_code = wlist.change_title(new_title=wlist_title)


bot.run(os.getenv('TOKEN'))
