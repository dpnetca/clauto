#!/usr/bin/env python

"""
Simple script to post a message to a teams room
"""

import os
import requests


api_url = "https://webexapis.com/v1/messages"
access_token = os.getenv("WEBEX_TOKEN")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

body = {"toPersonEmail": "tofrench@webex.bot", "text": "Hello"}


response = requests.post(url=api_url, headers=headers, json=body)

print(f"Status: {response.status_code}")
print(response.text)
