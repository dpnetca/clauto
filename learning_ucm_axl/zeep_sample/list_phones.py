"""
Connect to UCM read list of configured phones and display some
Information about the phones to the screen

Author: Denis Pointer
Website: dpnet.ca
"""

import os
from time import time

from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Transport
from zeep.plugins import HistoryPlugin

from dotenv import load_dotenv

# Disable insecure SSL warnings
import urllib3

st = time()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Load Environmental Variable
wsdl = os.getenv("WSDL_FILE")
username = os.getenv("UCM_USERNAME")
password = os.getenv("UCM_PASSWORD")
ucm_pub_url = f'https://{os.getenv("UCM_PUB_ADDRESS")}:8443/axl/'

print(f"init: {time() - st}s")
# Create Session, do not verify certificate, enable basic auth
session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)

# create transport with our session and 10 second timeout
transport = Transport(session=session, timeout=10)

history = HistoryPlugin()

# crete the Zeep client
client = Client(wsdl, transport=transport, plugins=[history])

# create the service proxy pointint to our UCM
service = client.create_service(
    binding_name="{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
    address=ucm_pub_url,
)

print(f"Zeep Setup: {time() - st}s")
# % is used for wildcard matcing any number of characters
list_phone_data = {"searchCriteria": {"name": "%"}, "returnedTags": {}}

phones = service.listPhone(**list_phone_data)
print(f"phone List: {time() - st}s")
for phone in phones["return"]["phone"]:
    # all fields are None exept uuid, use uuid to get phone details
    phone_detail = service.getPhone(uuid=phone["uuid"])

    # print some information about the phone
    print(f'name: {phone_detail["return"]["phone"]["name"]}')
    print(f'description: {phone_detail["return"]["phone"]["description"]}')
    print(f'model: {phone_detail["return"]["phone"]["model"]}')
    for line in phone_detail["return"]["phone"]["lines"]["line"]:
        print(f"Line {line['index']}: {line['dirn']['pattern']}")
    print()
print(f"Done: {time() - st}s")
