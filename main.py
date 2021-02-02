#!/usr/bin/python3

import json
from time import sleep

from notion.client import NotionClient

CONTROL_PANEL_URL = 'https://www.notion.so/d5e3513e606a4861ac5565c0229d115f?v=b1f178b8e1f543c28b52d31a0c1e07ec'
ALL_INGREDIENTS_URL = 'https://www.notion.so/39444bd43f9547fbab65d928fd2e1c31?v=3060a61f614d40d78232298cb2468465'
RESTOCK_URL = 'https://www.notion.so/39444bd43f9547fbab65d928fd2e1c31?v=56b9c57f15644b58a8a541d60575d644'

KEYS_PATH = 'keys.json'

with open(KEYS_PATH) as file:
    data = json.load(file)
token = data['token']

client = NotionClient(token_v2=token)
control_panel = client.get_collection_view(CONTROL_PANEL_URL)


def button_callback(f):
    def g(record, difference):
        change = difference[0]
        if (change[0] == 'change' and 'LPjR' in change[1] or \
            change[0] == 'add' and 'LPjR' in change[2][0]) and \
           record.on:
            print(f"Callback received for {record.name}.")
            record.show = False
            loading = control_panel.collection.get_rows(search=record.name + " (")[0]
            loading.show = True
            f()
            loading.show = False
            record.on = False
            record.show = True
    return g


@button_callback
def restock():
    to_restock = client.get_collection_view(RESTOCK_URL)
    for row in to_restock.collection.get_rows():
        if row.done:
            row.stock = "Full"
            row.done = False
        if row.needs_purchasing:
            row.needs_purchasing = False


def sync_icons():
    ingredients = client.get_collection_view(ALL_INGREDIENTS_URL)
    for row in ingredients.collection.get_rows():
        if row.emoji != row.icon:
            row.emoji = row.icon


def main():
    restock_button = control_panel.collection.get_rows(search="Restock Items")[0]
    restock_button.add_callback(restock)

    print("Listening...")
    while True:
        sleep(0.5)
        restock_button.refresh()


if __name__ == '__main__':
    main()
