#!/usr/bin/env python
"""
Add partition to CSS
"""

import os
import sys

from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Transport
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault

from dotenv import load_dotenv

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Load Environmental Variable
wsdl = os.getenv("WSDL_FILE")
username = os.getenv("UCM_USERNAME")
password = os.getenv("UCM_PASSWORD")
ucm_pub_url = f'https://{os.getenv("UCM_PUB_ADDRESS")}:8443/axl/'

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

css_name = "dp-test-css"
get_css_resp = service.getCss(name=css_name)

print("ORIGINAL CSS MEMBERS:")
print(get_css_resp["return"]["css"]["members"])

print("\n", "=" * 20, "\n")

css_uuid = get_css_resp["return"]["css"]["uuid"]
# print(css_uuid)

pt_name = "dp-test-pt"
pt_found = False
if get_css_resp["return"]["css"]["members"]:
    for member in get_css_resp["return"]["css"]["members"]["member"]:
        if member["routePartitionName"]["_value_1"] == pt_name:
            pt_found = True
            break

if not pt_found:
    print("partition is not in CSS")
    sys.exit(1)

get_pt_resp = service.getRoutePartition(name=pt_name)
pt_uuid = get_pt_resp["return"]["routePartition"]["uuid"]
# print(pt_uuid)

update_data = {
    "uuid": css_uuid,
    "removeMembers": {
        "member": [{"routePartitionName": {"uuid": pt_uuid}, "index": "1"}]
    },
}

try:
    update_resp = service.updateCss(**update_data)
    # print(update_resp)
except Fault as f:
    print(f"update failed: {f}")
    sys.exit(1)

get_css_resp = service.getCss(name=css_name)

print("UPDATED CSS MEMBERS:")
print(get_css_resp["return"]["css"]["members"])
