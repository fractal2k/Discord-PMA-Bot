import re
import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor


class NLPEngine():
    """Handles communication with Hugging Face's API and general NLP utilities"""

    def __init__(self):
        self.url = 'https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-1'
        self.headers = {'Authorization': f"Bearer {os.getenv('HF_TOKEN')}"}
        self.action_labels = ['add', 'check', 'update', 'remove']
        self.location_labels = ['in tray', 'waiting list',
                                'today\'s agenda', 'reading list', 'areas of focus']

    def post(self, data):
        """Generic post request method to send request to Hugging Face API"""
        return requests.post(self.url, headers=self.headers, data=data)

    def get_intent(self, text):
        """Classify intent of user text"""
        payloads = self.get_payloads(text)
        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(self.post, payloads))

        for response in responses:
            if response.status_code == 503:
                raise RuntimeError(
                    f'My natural language engine that helps me understand what you say is still loading. Please try again in {int(json.loads(response.content.decode("utf-8"))["estimated_time"])} seconds')
        return [json.loads(response.content.decode('utf-8'))['labels'][0] for response in responses]

    def get_payloads(self, text):
        """Generates payloads for action and location classification"""
        return [json.dumps({
            'inputs': text,
            'parameters': {'candidate_labels': self.action_labels,
                           'hypothesis_template': 'The action that the user wants to perform is {}.'}
        }),
            json.dumps({
                'inputs': text,
                'parameters': {'candidate_labels': self.location_labels,
                               'hypothesis_template': 'The user wants to work with {}.'}
            })]

    def extract_items(self, msg):
        """Extracts title of the book surrounded by double/single quotes"""
        # TODO: Create an entity extraction nlp pipeline for this
        items = re.findall('"[\w\s,?!\-]*"|\'[\w\s,?!\-]*\'', msg)
        return [item[1:-1] for item in items]
