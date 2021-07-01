import os
import json
import requests
# from dotenv import load_dotenv
# load_dotenv()

# TODO: Modularise code properly using classes and refactor it


def get_reading_queue():
    """Retrieves the reading queue from my notion page"""
    url = f"https://api.notion.com/v1/blocks/{os.getenv('NOTION_READING_QUEUE')}/children?page_size=50"
    headers = {
        'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}"}
    response = json.loads(requests.get(url, headers=headers).text)
    books = response['results'][2:]

    titles = []
    for idx, book in enumerate(books, 1):
        titles.append(str(idx) + '. ' +
                      book['bulleted_list_item']['text'][0]['text']['content'])

    return titles


def get_in_tray():
    '''Gets all elements in the in tray'''
    url = f"https://api.notion.com/v1/blocks/{os.getenv('NOTION_IN_TRAY')}/children"
    headers = {
        'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}"}
    response = json.loads(requests.get(url, headers=headers).text)
    num_elements = len(response['results'])
    result = []

    if num_elements > 0:
        result = [elem['bulleted_list_item']['text'][0]
                  ['text']['content'] for elem in response['results']]

    return result


def get_todays_agenda():
    '''Gets all elements in today's agenda'''
    url = f"https://api.notion.com/v1/blocks/{os.getenv('NOTION_NEXT_ACTIONS')}/children"
    headers = {
        'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}"}
    response = json.loads(requests.get(url, headers=headers).text)
    # TODO: Make this more dynamic to incorporate what project each task refers to and if there's a time attached to it
    result = [elem['bulleted_list_item']['text'][0]['plain_text']
              for elem in response['results'][1:-1]]

    return result


def add_book(titles):
    """Adds the given book title to the reading list"""
    url = f"https://api.notion.com/v1/blocks/{os.getenv('NOTION_READING_QUEUE')}/children"
    headers = {
        'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}", 'Content-Type': 'application/json'}
    children = []
    for title in titles:
        children.append(create_bullet(title[1:-1]))
    data = json.dumps({'children': children})
    response = requests.patch(url, headers=headers, data=data)
    status_code = response.status_code

    if status_code == 200:
        result = ('All good!', 'The book has been added to your reading list')
    else:
        result = ('Looks like something went wrong',
                  f'Error code: {status_code}')

    return result


def change_in_tray_title(new_title, debug=False):
    '''Changes the background color of in tray page'''
    url = f"https://api.notion.com/v1/pages/{os.getenv('NOTION_IN_TRAY')}"
    headers = {
        'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}", 'Content-Type': 'application/json'}
    data = {
        'properties': {
            'title': {
                'title': [
                    {
                        'type': 'text',
                        'plain_text': new_title,
                        'text': {
                            'content': new_title
                        }
                    }
                ]
            }
        }
    }
    data = json.dumps(data)
    response = requests.patch(url, headers=headers, data=data)

    if debug:
        return json.loads(response.text)

    status_code = response.status_code

    return status_code


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


# if __name__ == '__main__':
#     print(get_todays_agenda())
