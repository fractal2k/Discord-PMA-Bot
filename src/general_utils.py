import os
import json
import discord
import requests
from datetime import datetime


def get_quote():
    url = 'https://zenquotes.io/api/random'
    response = json.loads(requests.get(url).text)
    return response[0]['q'] + '\n- ' + response[0]['a']


def parse_top3(todays_agenda):
    top3_strings = []
    for i, item in enumerate(todays_agenda[:3], 1):
        item_desc = f'{i}. {item["task"].strip()}'
        if item['project'] != '':
            item_desc += f' from {item["project"]}'
        if item['date'] != '':
            deadline = datetime.fromisoformat(item['date']).ctime()
            item_desc += f'. Deadline: {deadline}'
        top3_strings.append(item_desc)

    return '\n'.join(top3_strings)
