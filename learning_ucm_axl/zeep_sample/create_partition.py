#!/usr/bin/env python
"""
Create a new partition
"""

import os
import sys

from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Transport
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault

from dotenv import load_dotenv

# Disable insecure SSL warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Load Environmental Variable
wsdl = os.getenv("WSDL_FILE")
username = os.getenv("UCM_USERNAME")
password = os.getenv("UCM_PASSWORD")
ucm_pub_url = f'https://{os.getenv("UCM_PUB_ADDRESS")}:8443/axl/'

# Create Session, do not verify certificate, enable basic auth
session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)

transport = Transport(session=session, timeout=10)

history = HistoryPlugin()

client = Client(wsdl=wsdl, transport=transport, plugins=[history])

service = client.create_service(
    binding_name="{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
    address=ucm_pub_url,
)

add_partition_data = {
    "name": "dp-test-pt",
    "description": "DP test partition added with AXL",
}

try:
    add_pt_resp = service.addRoutePartition(add_partition_data)
    print(add_pt_resp)
except Fault as f:
    print(f"unable to add parition: {f}")
    sys.exit(1)

try:
    get_pt_resp = service.getRoutePartition(uuid=add_pt_resp["return"])
    print(get_pt_resp)
except Fault as f:
    print(f"unable to get partition: {f}")
