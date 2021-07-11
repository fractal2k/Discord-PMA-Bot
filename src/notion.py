import re
import os
import json
import requests
from datetime import datetime


class Notion():
    """Base class for all Notion related objects"""

    def __init__(self):
        self.base_url = 'https://api.notion.com/v1/'
        self.base_headers = {
            'Authorization': f"Bearer {os.getenv('NOTION_SECRET')}",
            'Notion-Version': '2021-05-13'
        }

    def get(self, url):
        """Generic get request method"""
        return json.loads(requests.get(url, headers=self.base_headers).text)

    def patch(self, url, data):
        """Generic patch request method"""
        headers = self.base_headers.copy()
        headers['Content-Type'] = 'application/json'
        return requests.patch(url, headers=headers, data=data)

    def create_bullet(self, text):
        """Returns a notion bullet point object with the text given"""
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


class ReadingList(Notion):
    """Reading list wrapper class for notion"""

    def __init__(self):
        super().__init__()
        self.url = self.base_url + \
            f'blocks/{os.getenv("NOTION_READING_QUEUE")}/children'

    def get_list(self, debug=False):
        """Retrieves reading list from notion"""
        response = super().get(self.url)

        if debug:
            return response

        # [2:] because there's two block at the start of the page that are unwanted
        books = response['results'][2:]

        titles = []
        if len(books) > 0:
            titles = [book['bulleted_list_item']['text']
                      [0]['plain_text'] for book in books]

        return titles

    def add_book(self, books, debug=False):
        """Add given list of book to the reading list"""
        # [1:-1] because re.findall extracts the double quotes as well
        children = [super(ReadingList, self).create_bullet(book)
                    for book in books]
        data = json.dumps({'children': children})
        response = super().patch(self.url, data=data)

        if debug:
            return json.loads(response.text)

        return response.status_code


class InTray(Notion):
    """In tray wrapper class for Notion"""
    # Add dynamic parsing to account for urls

    def __init__(self):
        super().__init__()
        self.url = self.base_url + \
            f'blocks/{os.getenv("NOTION_IN_TRAY")}/children'
        self.page_url = self.base_url + f'pages/{os.getenv("NOTION_IN_TRAY")}'

    def get_tray(self, debug=False):
        """Gets the contents of the in tray from notion"""
        response = super().get(self.url)

        if debug:
            return response

        tray = []
        if len(response['results']) > 0:
            tray = [elem['bulleted_list_item']['text'][0]['plain_text']
                    for elem in response['results']]

        return tray

    def add_item(self, items, debug=False):
        """Add items to the in tray"""
        children = [super(InTray, self).create_bullet(item) for item in items]
        data = json.dumps({'children': children})
        response = super().patch(self.url, data=data)

        if debug:
            return json.loads(response.text)

        return response.status_code

    def change_title(self, new_title, debug=False):
        """Changes title of in tray page"""
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
        response = super().patch(self.page_url, data=data)

        if debug:
            return json.loads(response.text)

        return response.status_code


class WaitingList(Notion):
    """Waiting list wrapper class for Notion"""

    def __init__(self):
        super().__init__()
        self.url = self.base_url + \
            f'blocks/{os.getenv("NOTION_WAITING")}/children'
        self.page_url = self.base_url + f'pages/{os.getenv("NOTION_WAITING")}'

    def get_list(self, debug=False):
        """Retrieves waiting list contents from notion"""
        response = super().get(self.url)

        if debug:
            return response

        wlist = []
        if len(response['results']) > 0:
            wlist = [elem['bulleted_list_item']['text'][0]['plain_text']
                     for elem in response['results']]

        return wlist

    def add_item(self, items, debug=False):
        children = [super(WaitingList, self).create_bullet(item)
                    for item in items]
        data = json.dumps({'children': children})
        response = super().patch(self.url, data=data)

        if debug:
            return json.loads(response.text)

        return response.status_code

    def change_title(self, new_title, debug=False):
        """Method to change title of waiting list page"""
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
        response = super().patch(self.page_url, data=data)

        if debug:
            return json.loads(response.text)

        return response.status_code


class TodaysAgenda(Notion):
    """Today's agenda wrapper class for Notion"""

    def __init__(self):
        super().__init__()
        self.url = self.base_url + \
            f'blocks/{os.getenv("NOTION_NEXT_ACTIONS")}/children'

    def get_agenda(self, debug=False):
        """Retrieves today's agenda from notion"""
        response = super().get(self.url)

        if debug:
            return response

        return self.parse_agenda_response(response)

    def parse_agenda_response(self, response):
        """Dynamically parses agenda items from json response"""
        result = []

        for elem in response['results'][1:-1]:
            text_array = elem['bulleted_list_item']['text']
            result_elem = {'task': '', 'project': '', 'date': ''}

            for text_object in text_array:
                if text_object['type'] == 'text':
                    result_elem['task'] += text_object['plain_text']
                elif text_object['type'] == 'mention' and text_object['mention']['type'] == 'page':
                    result_elem['project'] = text_object['plain_text']
                elif text_object['type'] == 'mention':
                    result_elem['date'] = text_object['mention']['date']['start']
            result.append(result_elem)

        return self.create_strings(result)

    def create_strings(self, tagenda):
        """Convert items in today's agenda dict in string format"""
        # TODO: Incorporate this method's functionality into parse_agenda_response()
        display_strings = []
        for item in tagenda:
            item_desc = f'{item["task"].strip()}'
            if item['project'] != '':
                item_desc += f' from {item["project"]}'
            if item['date'] != '':
                deadline = datetime.fromisoformat(item['date']).ctime()
                item_desc += f'. Deadline: {deadline}'
            display_strings.append(item_desc)

        return display_strings


class AreasOfFocus(Notion):
    """Areas of focus wrapper class for Notion"""

    def __init__(self):
        super().__init__()
        self.url = self.base_url + f'blocks/{os.getenv("NOTION_AOF")}/children'

    def get_aof(self, debug=False):
        """Retrieves areas of focus from Notion"""
        response = super().get(self.url)

        if debug:
            return response

        return self.aof_response_parser(response)

    def aof_response_parser(self, response):
        """Parses areas of focus elements from json response"""
        aof = {
            'personal': [],
            'professional': []
        }
        if len(response['results']) > 0:
            key = 'personal'
            for elem in response['results'][1:]:
                if elem['type'].startswith('heading'):
                    key = 'professional'
                    continue
                aof[key].append(elem['bulleted_list_item']
                                ['text'][0]['plain_text'])

        return aof
