#!/usr/bin/env python

"""
Simple script to get list of Webex Teams Rooms
"""

import requests
import os

api_url = "https://webexapis.com/v1/rooms"
access_token = os.getenv("WEBEX_TOKEN")
sortby = "lastactivity"
max_rooms = "8"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

query = {"sortBy": sortby, "max": max_rooms}

response = requests.get(url=api_url, headers=headers, params=query)

print(f"Status: {response.status_code}")
print("-" * 20)
rooms = response.json()
for room in rooms["items"]:
    print(f"ID: {room['id']}")
    print(f"Title: {room['title']}")
    print("-" * 20)
