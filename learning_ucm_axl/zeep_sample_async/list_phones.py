"""
Connect to UCM read list of configured phones and display some
Information about the phones to the screen

Author: Denis Pointer
Website: dpnet.ca
"""

# TODO: idenfiy cause of periodic and frequent failure getting phone details

import os
from time import time
import asyncio

from aiohttp import ClientSession, BasicAuth, TCPConnector
from zeep import Client
from zeep.asyncio import AsyncTransport
from zeep.exceptions import Fault

from dotenv import load_dotenv


async def get_phone_list(service):
    # % is used for wildcard matcing any number of characters
    list_phone_data = {"searchCriteria": {"name": "%"}, "returnedTags": {}}
    phone_list = await service.listPhone(**list_phone_data)
    # print(phone_list["return"]["phone"])
    # for phone in phone_list["return"]["phone"]:
    #     print(phone["uuid"])
    return phone_list["return"]["phone"]


async def get_phone_detail(service, uuid):
    phone_detail = await service.getPhone(uuid=uuid)
    return phone_detail["return"]["phone"]


async def get_phone_list_detail(service, phone_list):
    tasks = []
    for phone in phone_list:
        tasks.append(get_phone_detail(service, phone["uuid"]))
        # print(phone["uuid"])
    phone_details = await asyncio.gather(*tasks, return_exceptions=True)
    for phone_detail in phone_details:
        if type(phone_detail) == Fault:
            print(phone_detail)
            # TODO add debugging here to see why failing
            continue
        print(f'name: {phone_detail["name"]}')
        print(f'description: {phone_detail["description"]}')
        print(f'model: {phone_detail["model"]}')
        for line in phone_detail["lines"]["line"]:
            print(f"Line {line['index']}: {line['dirn']['pattern']}")
        print()


async def main():
    st = time()
    loop = asyncio.get_event_loop()
    load_dotenv()

    # Load Environmental Variable
    wsdl = os.getenv("WSDL_FILE")
    username = os.getenv("UCM_USERNAME")
    password = os.getenv("UCM_PASSWORD")
    ucm_pub_url = f'https://{os.getenv("UCM_PUB_ADDRESS")}:8443/axl/'

    print(f"init: {time() - st}s")

    # Create Session, do not verify certificate, enable basic auth
    # ISSUE, zeep not using cookies, authenticating every time
    # authentication is rate limited
    connector = TCPConnector(ssl=False, limit=5)
    auth = BasicAuth(username, password)
    async with ClientSession(connector=connector, auth=auth) as session:
        transport = AsyncTransport(loop=loop, session=session, timeout=10)
        client = Client(wsdl, transport=transport)

        # create the service proxy pointint to our UCM
        service = client.create_service(
            binding_name="{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            address=ucm_pub_url,
        )
        print(f"Zeep Setup: {time() - st}s")
        phone_list = await get_phone_list(service)
        # print(client.transport.session)
        print(f"phone List: {time() - st}s")
        await get_phone_list_detail(service, phone_list)
        print(f"Done: {time() - st}s")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
