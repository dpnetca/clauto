#!/usr/bin/env python

"""
Simple script to post a message to a teams room
"""

import os
import requests


api_url = "https://webexapis.com/v1/messages"
access_token = os.getenv("WEBEX_TOKEN")
room_id = os.getenv("WEBEX_BOT_ROOMID")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

messages = [
    "**Warning!**",
    "_Warning!_",
    "[Danger, Will Robinson](https://en.wikipedia.org/)",
]
for message in messages:
    body = {
        "roomId": room_id,
        "markdown": message,
    }
    response = requests.post(url=api_url, headers=headers, json=body)

    print(f"Status: {response.status_code}")
    print(response.text)
    print("-" * 20)
