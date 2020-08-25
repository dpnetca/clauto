#!/usr/bin/env python
"""
Simple Chatops Bot
"""

import os
import sys
import requests
import argparse


def send_it(token, room_id, message):
    api_url = "https://webexapis.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    data = {"roomId": room_id, "text": message}
    response = requests.post(url=api_url, headers=headers, json=data)

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="chatops.py")
    parser.add_argument(
        "-m", "--message", help="message to post", required=True
    )
    parser.add_argument("-r", "--room_id", help="room ID", required=False)
    parser.add_argument(
        "-t", "--token", help="access token or can use WEBEX_BOT_TOKEN env"
    )
    args = parser.parse_args()

    env_token = os.getenv("WEBEX_BOT_TOKEN")
    env_roomid = os.getenv("WEBEX_BOT_ROOMID")
    access_token = args.token if args.token else env_token
    room_id = args.room_id if args.room_id else env_roomid

    if not access_token:
        print("Define access token")
        sys.exit(2)

    response = send_it(access_token, room_id, args.message)
    if response.status_code == 200:
        print("message posted")
    else:
        print("messsage failed")
        print(f"Status: {response.status_code}")
        print(response.text)
