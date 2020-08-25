#!/usr/bin/env python
"""
Connect to UCM read list of configured phones and display some
Information about the phones to the screen

Author: Denis Pointer
Website: dpnet.ca
"""
import os

import asyncio
import aiohttp

from lxml import etree as ET
from lxml.builder import ElementMaker
import xmltodict

from dotenv import load_dotenv


class Soap:
    """
    Defined class to store common data
    """

    def __init__(self, url=None, auth=None):
        load_dotenv()

        if url:
            self.url = url
        else:
            self.url = f'https://{os.getenv("UCM_PUB_ADDRESS")}:8443/axl/'

        if auth:
            self.auth = auth
        else:
            username = os.getenv("UCM_USERNAME")
            password = os.getenv("UCM_PASSWORD")
            self.auth = aiohttp.BasicAuth(username, password)

        # consider passing as perameters?
        self.soap_ver = "12.5"

        self.soap_ns = "http://schemas.xmlsoap.org/soap/envelope/"
        self.axl_ns = f"http://www.cisco.com/AXL/API/{self.soap_ver}"
        self.ns_map = {"soapenv": self.soap_ns, "ns0": self.axl_ns}
        self.cookies = None

    async def send_request(self, session, soap_action, envelope_string):
        # print(f"running {soap_action}")
        soap_header = f'"CUCM:DB ver={self.soap_ver} {soap_action}"'

        header = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": soap_header,
        }
        if self.cookies:
            auth = None
        else:
            auth = self.auth
        result = await session.post(
            url=self.url,
            headers=header,
            auth=auth,
            data=envelope_string,
            ssl=False,
            cookies=self.cookies,
        )
        xml = await result.text()
        # print(result.status)
        self.cookies = result.cookies
        xml_dict = xmltodict.parse(xml)
        xml_body = xml_dict["soapenv:Envelope"]["soapenv:Body"]
        xml_return = xml_body[f"ns:{soap_action}Response"]["return"]

        return xml_return


async def main():
    ucm_pub = Soap()

    soap_action = "listPhone"
    env_dict = {
        "soapenv:Envelope": {
            "@xmlns:soapenv": ucm_pub.soap_ns,
            "@xmlns:ns0": ucm_pub.axl_ns,
            "soapenv:Body": {
                f"ns0:{soap_action}": {
                    "searchCriteria": {"name": "%"},
                    "returnedTags": None,
                }
            },
        }
    }
    envelope = xmltodict.unparse(env_dict)
    conenctor = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=conenctor) as session:
        phone_list = await ucm_pub.send_request(session, soap_action, envelope)

        soap_action = "getPhone"
        tasks = []
        for phone in phone_list["phone"]:
            soap = ElementMaker(
                namespace=ucm_pub.soap_ns, nsmap=ucm_pub.ns_map
            )
            envelope = soap.Envelope()

            ns = ElementMaker(namespace=ucm_pub.axl_ns)
            elem = ElementMaker()

            getPhone = ns(soap_action)
            uuid = elem("uuid")
            uuid.text = phone["@uuid"]

            body = soap.Body()
            getPhone.append(uuid)
            body.append(getPhone)
            envelope.append(body)

            envelope_string = ET.tostring(envelope)
            tasks.append(
                ucm_pub.send_request(session, soap_action, envelope_string)
            )

        phone_details = await asyncio.gather(*tasks, return_exceptions=True)
        for phone in phone_details:
            print(phone["phone"]["name"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
