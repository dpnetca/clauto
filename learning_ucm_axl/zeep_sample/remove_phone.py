"""
Connect to UCM add remove phone with name SEPAAAABBBB0001

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

# change name to delete a different phone
phone_name = "SEPAAAABBBB0001"

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
phone_details = {
    "name": phone_name,
}


try:
    phone = service.removePhone(**phone_details)
    print("phone removed")
except Fault as f:
    print(f"Unable to add Phone: {f}")
    sys.exit(1)
