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


def get_all_tags():
    token = get_access_token()
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
        tmp_tags = content["data"]
        for tag in tmp_tags:
            tag_id = tag["tag_id"]
            del tag["tag_id"]
            all_tags[tag_id] = tag

    return all_tags


tags = get_all_tags()
with open("json/tags.json", 'w', encoding='utf-8') as f:
    dump(tags, f, ensure_ascii=False, indent=4)

with open("json/tags.min.json", 'w', encoding='utf-8') as f:
    dump(tags, f, ensure_ascii=False)

with open("json/tags_ascii.json", 'w', encoding='utf-8') as f:
    dump(tags, f, ensure_ascii=True, indent=4)

with open("json/tags_ascii.min.json", 'w', encoding='utf-8') as f:
    dump(tags, f, ensure_ascii=True)
