#!/usr/bin/env python
"""
Connect to UCM read list of configured phones and display some
Information about the phones to the screen

Author: Denis Pointer
Website: dpnet.ca
"""

from lxml import etree as ET
from lxml.builder import ElementMaker
import xmltodict

from helpers import Soap

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
phone_list = ucm_pub.send_request(soap_action, envelope)

soap_action = "getPhone"

for phone in phone_list["phone"]:
    soap = ElementMaker(namespace=ucm_pub.soap_ns, nsmap=ucm_pub.ns_map)
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
    phone_details = ucm_pub.send_request(soap_action, envelope_string)
    print(phone_details["phone"]["name"])
