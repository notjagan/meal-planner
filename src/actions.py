#!/usr/bin/python3

import json
import argparse
from datetime import datetime, timedelta

from notion.client import NotionClient
from notion.collection import NotionDate

INGREDIENTS_URL = 'https://www.notion.so/39444bd43f9547fbab65d928fd2e1c31?v=3060a61f614d40d78232298cb2468465'
SCHEDULE_URL = 'https://www.notion.so/1e11415ec8444439b91400531a5a925c?v=c6145fbc64f74a538d48fcbc59a235f6'

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


def archive_schedule():
    schedule = client.get_collection_view(SCHEDULE_URL)
    this_week = {}
    next_week = {}
    for row in schedule.collection.get_rows():
        if row.this_week:
            this_week[row.day] = row
        elif row.next_week:
            next_week[row.day - 7] = row

    weekday = datetime.today().weekday() + 1 % 7
    for index, current in this_week.items():
        ahead = next_week[index]

        delta = timedelta(days=current.day - weekday)
        date = datetime.today() + delta
        archive = schedule.collection.add_row()
        archive.name = date.strftime("%m/%d")
        archive.manual_date = NotionDate(date)
        archive.lunch = current.lunch
        archive.snack = current.snack
        archive.dinner = current.dinner

        current.lunch = ahead.lunch
        current.snack = ahead.snack
        current.dinner = ahead.dinner
        ahead.lunch = []
        ahead.snack = []
        ahead.dinner = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--restock', action='store_true')
    parser.add_argument('--icons', action='store_true')
    parser.add_argument('--archive', action='store_true')
    args = parser.parse_args()

    if args.restock:
        print("Restocking items...")
        restock()
        print("Restocking complete.")
    if args.icons:
        print("Syncing icons...")
        sync_icons()
        print("Icons synced.")
    if args.archive:
        print("Archiving schedule...")
        archive_schedule()
        print("Schedule archived.")


if __name__ == '__main__':
    main()
