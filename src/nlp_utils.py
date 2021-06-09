import re
import os
import json
import discord
import requests
from notion_utils import get_reading_queue, add_book


def query_intent_classifier(sequence):
    """Sends a get request to hugginface's zero shot text classification model API"""
    payload = {
        'inputs': sequence,
        'parameters': {'candidate_labels': ['add', 'check', 'update', 'remove'],
                       'hypothesis_template': 'The action that the user wants to perform is {}.'}
    }

    url = 'https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-1'
    headers = {'Authorization': f"Bearer {os.getenv('HF_TOKEN')}"}
    data = json.dumps(payload)
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 503:
        return 'Error: Please wait, I\'m loading my natural language engine that helps me understand what you say.'

    return json.loads(response.content.decode('utf-8'))['labels'][0]


def query_response_handler(label, message):
    """Executes actions according to what the intent of the user is"""
    if label == 'add':
        titles = extract_book_title(message)
        title, desc = add_book(titles)

        return {
            'title': title,
            'description': desc,
            'color': discord.Color.orange().value
        }
    elif label == 'check':
        titles = get_reading_queue()
        return {
            'title': 'Your Reading Queue',
            'description': '\n'.join(titles),
            'color': discord.Color.orange().value
        }
    elif label == 'update':
        # Cannot be done yet because Notion's API doesn't support it
        pass
    elif label == 'remove':
        # Cannot be done yet because Notion's API doesn't support it
        pass


def extract_book_title(message):
    """Extracts title of the book surrounded by double/single quotes"""
    titles = re.findall('"[\w\s,?!\-]*"|\'[\w\s,?!\-]*\'', message)
    return titles
