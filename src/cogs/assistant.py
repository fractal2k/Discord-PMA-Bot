import os
import discord
from discord.ext import commands
from nlp_utils import query_intent_classifier, query_response_handler


class Assistant(commands.Cog):
    """Cog containing PMA functionality of the bot"""

    def __init__(self, client):
        self.client = client
        self.command_list = ['hi', 'hello', 'hey', 'inspire', 'clear']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('pma') and message.content[4:] not in self.command_list:
            response = query_intent_classifier(message.content[4:])
            if response.startswith('Error'):
                result = {
                    'title': 'Oops!',
                    'description': response,
                    'color': discord.Color.orange().value
                }
            else:
                result = query_response_handler(response, message.content[4:])

            await message.channel.send(embed=discord.Embed.from_dict(result))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        """Suppressing all no command found errors because it triggers every time the upper method is invoked"""
        pass


def setup(client):
    client.add_cog(Assistant(client))
