#!/usr/bin/env python
"""
Do several actions, pause between each and wait for user to hit enter
to allow verification in CUCM web interface to view the changes
Actions:
  * Add Partition dpnetca-dn-pt
  * Add Device CSS dpnetca-device-css with parition

  * Remove Device CSS dpnetca-device-css
  * Remove Partition dpnetca-dn-pt

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


def setup_client_service():
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

    # crete the Zeep client
    client = Client(wsdl, transport=transport, plugins=[history])

    # create the service proxy pointint to our UCM
    service = client.create_service(
        binding_name="{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
        address=ucm_pub_url,
    )
    return client, service


def main():
    # this probably isn't good practice ...
    client, service = setup_client_service()

    # Setup Factories
    axl_factory = client.type_factory("ns0")
    # xsd_factory = client.type_factory("xsd")

    ############################
    # Define Items to be added #
    ############################

    # Use factories to create partition "dpnetca-dn-pt"
    dn_partition = axl_factory.XRoutePartition(
        name="dpnetca-dn-pt",
        description="Route Pattern added by dpnetca big sample script",
    )

    # define CSS as a dict
    device_css = {
        "name": "dpnetca-device-css",
        "description": "Device CSS added by dpnetca big sample script",
        "members": {
            "member": [
                {
                    "routePartitionName": {"_value_1": "dpnetca-dn-pt"},
                    "index": 1,
                }
            ]
        },
    }

    #############
    # ADD ITEMS #
    #############

    # Add parition, or display error and exit
    try:
        service.addRoutePartition(dn_partition)
        print("\n" + "#" * 20)
        print("Partition Added")
        print("#" * 20 + "\n")

    except Fault as f:
        print(f"unable to add parition: {f}")
        sys.exit(1)

    input("Press ENTER to continue")

    # Add Device CSS with member partition
    try:
        service.addCss(device_css)
        print("\n" + "#" * 20)
        print("Device CSS Added")
        print("#" * 20 + "\n")

    except Fault as f:
        print(f"unable to Device CSS: {f}")
        sys.exit(1)

    input("Press ENTER to continue")

    ################
    # REMOVE ITEMS #
    ################

    try:
        service.removeCss(name=device_css["name"])
        print("\n" + "#" * 20)
        print("Device CSS Removed")
        print("#" * 20 + "\n")
    except Fault as f:
        print(f"unable to remove Device CSS: {f}")
        sys.exit(1)

    input("Press ENTER to continue")

    try:
        service.removeRoutePartition(name=dn_partition["name"])
        print("\n" + "#" * 20)
        print("Partition Removed")
        print("#" * 20 + "\n")
    except Fault as f:
        print(f"unable to remove parition: {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
