#!/usr/binenv python

import os

import requests
import xmltodict

from dotenv import load_dotenv

# Disable insecure SSL warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
            self.auth = requests.auth.HTTPBasicAuth(username, password)

        # consider passing as perameters?
        self.soap_ver = "12.5"

        self.soap_ns = "http://schemas.xmlsoap.org/soap/envelope/"
        self.axl_ns = f"http://www.cisco.com/AXL/API/{self.soap_ver}"
        self.ns_map = {"soapenv": self.soap_ns, "ns0": self.axl_ns}

        self.session = requests.session()

    def send_request(self, soap_action, envelope_string):
        soap_header = f'"CUCM:DB ver={self.soap_ver} {soap_action}"'

        header = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": soap_header,
        }
        if self.session.cookies:
            auth = None
        else:
            auth = self.auth
        result = self.session.post(
            url=self.url,
            headers=header,
            auth=auth,
            data=envelope_string,
            verify=False,
        )
        xml_dict = xmltodict.parse(result.text)
        action_response = xml_dict["soapenv:Envelope"]["soapenv:Body"]
        returned_value = action_response[f"ns:{soap_action}Response"]["return"]

        return returned_value
