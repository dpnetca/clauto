# AXL Learning Library

This is a misc collection of scripts that are created as part of a learning exercise for using python to integration with the Cisco Unified Communications Manager AP w/ AXL.

Somethings in this project are intentionally inconsistent. This is primarily a learning exerciese, I want to investigte and learn multiple options, and I am leaving multiple options in the code for future reference. Various libraries will be used for interaction with the API's. ZEEP makes things pretty easy, but is not condusive to learning. So, I will be looking at using ZEEP, ZEEP[ASYNC], as well as doing it manually with reqests annd aiohttp. for builging and parsing XML I am looking at using xml elementtree, lxml, and xmltodict.

## Primary Libraries:

- python-dotenv library used for UCM IP and credentials
- zeep used for AXL/SOAP
- zeep[async] used for asyncio capability with zeep and aiohttp
- Manual Parsing:
  - requests for http calls
  - lxml to build XML SOAP envelope
  - xmltodict to read responses
