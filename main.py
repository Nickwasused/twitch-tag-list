#!/bin/python3
from dotenv import load_dotenv
from json import loads, dump
from os import getenv
import requests

load_dotenv()

# https://dev.twitch.tv/docs/api/reference/#get-all-stream-tags


def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': getenv('CLIENT_ID'),
        'client_secret': getenv('CLIENT_SECRET'),
        'grant_type': 'client_credentials'
    }

    x = requests.post(url, json=data)
    return loads(x.content)["access_token"]


token = get_access_token()


def get_all_tags():
    tag_url = "https://api.twitch.tv/helix/tags/streams?first=100"
    all_tags = {}
    cursor = ""
    fetching = True

    while fetching:
        url = tag_url
        if cursor != "":
            url += f'&after={cursor}'
        x = requests.get(url, headers={
            'client-id': getenv('CLIENT_ID'),
            'Authorization': f'Bearer {token}'
        })

        content = loads(x.text)
        try:
            cursor = content["pagination"]["cursor"]
        except KeyError:
            fetching = False

        all_tags.update({tag["tag_id"]: {k: v for k, v in tag.items() if k != "tag_id"} for tag in content["data"]})

    return all_tags


tags = get_all_tags()
files = [
    ("json/tags.json", False, 4),
    ("json/tags.min.json", False, None),
    ("json/tags_ascii.json", True, 4),
    ("json/tags_ascii.min.json", True, None),
]

for filename, use_ascii, indent in files:
    with open(filename, "w", encoding="utf-8") as f:
        dump(tags, f, ensure_ascii=use_ascii, indent=indent)
