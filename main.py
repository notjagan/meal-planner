#!/usr/bin/python3

import json

from notion.client import NotionClient

INGREDIENTS_URL = 'https://www.notion.so/82e27313fcea4083bfdd46dc24c2d1f5?v=2e43d19c145d418d91ed8a741012f83b'
KEYS_PATH = 'keys.json'

with open(KEYS_PATH) as file:
    data = json.load(file)
token = data['token']

client = NotionClient(token_v2=token)
