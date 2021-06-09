import os
import json
import requests


def get_reading_queue():
    """Retrieves the reading queue from my notion page"""
    url = f"https://api.notion.com/v1/blocks/{os.getenv('NOTION_READING_QUEUE')}/children?page_size=50"
    headers = {'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}"}
    response = json.loads(requests.get(url, headers=headers).text)
    books = response['results'][2:]

    titles = []
    for idx, book in enumerate(books, 1):
        titles.append(str(idx) + '. ' +
                      book['bulleted_list_item']['text'][0]['text']['content'])

    return titles


def add_book(titles):
    """Adds the given book title to the reading list"""
    url = f"https://api.notion.com/v1/blocks/{os.getenv('NOTION_READING_QUEUE')}/children"
    headers = {'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}", 'Content-Type': 'application/json'}
    children = []
    for title in titles:
        children.append(create_bullet(title[1:-1]))
    data = json.dumps({'children': children})
    response = requests.patch(url, headers=headers, data=data)
    status_code = response.status_code

    if status_code == 200:
        result = ('All good!', 'The book has been added to your reading list')
    else:
        result = ('Looks like something went wrong', f'Error code: {status_code}')
    
    return result


def create_bullet(text):
    return {
        'object': 'block',
        'type': 'bulleted_list_item',
        'bulleted_list_item': {
            'text': [
                {
                    'type': 'text',
                    'text': {
                        'content': text
                    }
                }
            ]
        }
    }
