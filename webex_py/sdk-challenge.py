#!/usr/bin/env python
"""
Code challenge (optional)

To pass this challenge: create a room and post the below message into the room, using markdown syntax.

**I am an IT-Professional, and I have completed this challenge!!!**


"""

import os
from webexteamssdk import WebexTeamsAPI

message = "**I am an IT-Professional, and I have completed this challenge!!!**"

token = os.getenv("WEBEX_TOKEN")
api = WebexTeamsAPI(access_token=token)
room = api.rooms.create(title="WebEx SDK Challenge Room")
message = api.messages.create(roomId=room.id, markdown=message)
print(message)
