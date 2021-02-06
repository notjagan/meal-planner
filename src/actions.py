#!/usr/bin/python3

import json
import argparse

from notion.client import NotionClient

INGREDIENTS_URL = 'https://www.notion.so/39444bd43f9547fbab65d928fd2e1c31?v=3060a61f614d40d78232298cb2468465'

KEYS_PATH = 'keys.json'

with open(KEYS_PATH) as file:
    data = json.load(file)
token = data['token']

client = NotionClient(token_v2=token)


def restock():
    ingredients = client.get_collection_view(INGREDIENTS_URL)
    for row in ingredients.collection.get_rows():
        if row.done:
            row.stock = "Full"
            row.done = False
            if row.needs_purchasing:
                row.needs_purchasing = False


def sync_icons():
    ingredients = client.get_collection_view(INGREDIENTS_URL)
    for row in ingredients.collection.get_rows():
        if row.emoji != row.icon:
            row.emoji = row.icon


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--restock', action='store_true')
    parser.add_argument('--icons', action='store_true')
    args = parser.parse_args()

    if args.restock:
        print("Restocking items...")
        restock()
        print("Restocking complete.")
    if args.icons:
        print("Syncing icons...")
        sync_icons()
        print("Icons synced.")


if __name__ == '__main__':
    main()
