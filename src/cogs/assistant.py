import os
import discord
from notion import *
from discord.ext import commands
from nlp import NLPEngine


class Assistant(commands.Cog):
    """Cog containing PA functionality of the bot"""

    def __init__(self, client):
        self.client = client
        self.command_list = ['hi', 'hello', 'hey', 'inspire', 'clear']
        self.engine = NLPEngine()
        self.rlist = ReadingList()
        self.wlist = WaitingList()
        self.intray = InTray()
        self.tagenda = TodaysAgenda()
        self.aof = AreasOfFocus()
        self.embed_color = discord.Color.orange().value

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('pma') and message.content[4:] not in self.command_list:
            try:
                response = self.engine.get_intent(message.content[4:])
                result = self.fulfillment(response, message.content[4:])
            except RuntimeError as e:
                embed = self.get_embed('error')
                embed.description = e.__str__
                result = {'embed': embed}

            await message.channel.send(**result)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        """Suppressing all no command found errors because it triggers every time on_message() is invoked"""
        pass

    def fulfillment(self, labels, message):
        """Executes actions according to the intent of the user"""
        action, loc = labels

        if loc == 'in tray':
            return self.in_tray_handler(action, message)
        elif loc == 'waiting list':
            return self.waiting_handler(action, message)
        elif loc == 'today\'s agenda':
            return self.todays_agenda_handler(action)
        elif loc == 'reading list':
            return self.reading_list_handler(action, message)
        elif loc == 'areas of focus':
            return self.aof_handler(action)

    def in_tray_handler(self, action, msg):
        """Fulfillment method for intray related actions"""
        if action == 'check':
            tray = self.intray.get_tray()

            if len(tray) == 0:
                result = {'content': 'There\'s nothing in here.'}
            else:
                desc = '\n'.join(
                    [f'{idx}. {item}' for idx, item in enumerate(tray, 1)])
                embed = self.get_embed('intray-check')
                embed.description = desc
                result = {'embed': embed}

            return result
        elif action == 'add':
            items = self.engine.extract_items(msg)
            status_code = self.intray.add_item(items)

            if status_code == 200:
                embed = self.get_embed('intray-add')
            else:
                embed = self.get_embed('error')
                embed.description = f'Something went wrong. Error code: {status_code}'

            return {'embed': embed}

    def waiting_handler(self, action, msg):
        """Fulfillment method for waiting list related actions"""
        if action == 'check':
            wlist = self.wlist.get_list()

            if len(wlist) == 0:
                result = {'content': 'There\'s nothing here.'}
            else:
                desc = '\n'.join(
                    [f'{idx}. {item}' for idx, item in enumerate(wlist, 1)])
                embed = self.get_embed('wlist-check')
                embed.description = desc
                result = {'embed': embed}

            return result
        elif action == 'add':
            items = self.engine.extract_items(msg)
            status_code = self.wlist.add_item(items)

            if status_code == 200:
                embed = self.get_embed('wlist-add')
            else:
                embed = self.get_embed('error')
                embed.description = f'Something went wrong. Error code: {status_code}'

            return {'embed': embed}

    def todays_agenda_handler(self, action):
        """Fulfillment method for today's agenda related actions"""
        if action == 'check':
            tagenda = self.tagenda.get_agenda()

            if len(tagenda) == 0:
                result = {'content': 'Nothing.. here? Get some work done lol'}
            else:
                desc = '\n'.join(
                    [f'{idx}. {item}' for idx, item in enumerate(tagenda, 1)])
                embed = self.get_embed('tagenda-check')
                embed.description = desc
                result = {'embed': embed}

            return result

    def reading_list_handler(self, action, msg):
        """Fulfillment method for reading list related actions"""
        if action == 'check':
            rlist = self.rlist.get_list()

            if len(rlist) == 0:
                result = {
                    'content': 'Nothing here. Should probably get some books to read.'}
            else:
                embed = self.get_embed('rlist-check')
                desc = '\n'.join(
                    [f'{idx}. {book}' for idx, book in enumerate(rlist, 1)])
                embed.description = desc
                result = {'embed': embed}

            return result
        elif action == 'add':
            books = self.engine.extract_items(msg)
            status_code = self.rlist.add_book(books)

            if status_code == 200:
                embed = self.get_embed('rlist-add')
            else:
                embed = self.get_embed('error')
                embed.description = f'Something went wrong. Error code: {status_code}'

            return {'embed': embed}

    def aof_handler(self, action):
        """Fulfillment method for areas of focus related actions"""
        if action == 'check':
            aof = self.aof.get_aof()

            top3_personal = '\n'.join(
                [f'{idx}. {item}' for idx, item in enumerate(aof['personal'][:3], 1)])
            top3_professional = '\n'.join(
                [f'{idx}. {item}' for idx, item in enumerate(aof['professional'][:3], 1)])

            embed = self.get_embed('aof-check')
            embed.add_field(name='Personal', value=top3_personal, inline=False)
            embed.add_field(name='Professional',
                            value=top3_professional, inline=False)

            return {'embed': embed}

    def get_embed(self, type):
        """Get respective embed objects"""
        if type == 'error':
            embed = discord.Embed(
                title='Oops!',
                color=self.embed_color
            )
        elif type == 'rlist-check':
            embed = discord.Embed(
                title='Your reading list',
                color=self.embed_color
            )
        elif type == 'rlist-add':
            embed = discord.Embed(
                title='All good!',
                description='The book\'s been added to your reading list.',
                color=self.embed_color
            )
        elif type == 'tagenda-check':
            embed = discord.Embed(
                title='Today\'s agenda',
                color=self.embed_color
            )
        elif type == 'wlist-check':
            embed = discord.Embed(
                title='Your waiting list',
                color=self.embed_color
            )
        elif type == 'wlist-add':
            embed = discord.Embed(
                title='All good!',
                description='Your waiting list has been updated.',
                color=self.embed_color
            )
        elif type == 'intray-check':
            embed = discord.Embed(
                title='Here\'s your in tray',
                color=self.embed_color
            )
        elif type == 'intray-add':
            embed = discord.Embed(
                title='All good!',
                description='I\'ve added that to your in tray.',
                color=self.embed_color
            )
        elif type == 'aof-check':
            embed = discord.Embed(
                title='Your areas of focus',
                description='Here\'s your areas of focus.',
                color=self.embed_color
            )
        return embed


def setup(client):
    client.add_cog(Assistant(client))
