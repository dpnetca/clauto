"""
Connect to UCM add a new phone with minimum details

Author: Denis Pointer
Website: dpnet.ca
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

# create transport with our session and 10 second timeout
transport = Transport(session=session, timeout=10)

history = HistoryPlugin()

# create the Zeep client
client = Client(wsdl, transport=transport, plugins=[history])

# create the service proxy pointing to our UCM
service = client.create_service(
    binding_name="{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
    address=ucm_pub_url,
)

"""
There are many fields that can be set when adding A new phone
in the example below, descrition is optional, but all other
fields represent the minimum requried fields for adding a phone
"""
phone_details = {
    "name": "SEPAAAABBBB0001",
    "description": "DP Test Adding Phone from API",
    "product": "Cisco 8841",
    "class": "Phone",
    "protocol": "SIP",
    "protocolSide": "User",
    "devicePoolName": {"_value_1": "Default"},
    "commonPhoneConfigName": {"_value_1": "Standard Common Phone Profile"},
    "locationName": {"_value_1": "Hub_None"},
    "useTrustedRelayPoint": "Default",
    "builtInBridgeStatus": "Default",
    "packetCaptureMode": "None",
    "certificateOperation": "No Pending Operation",
    "deviceMobilityMode": "Default",
}

try:
    phone = service.addPhone(phone_details)
except Fault as f:
    print(f"Unable to add Phone: {f}")
    sys.exit(1)

print(phone)
