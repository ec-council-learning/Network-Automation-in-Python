#!/usr/bin/python -tt
# Project: ip_info
# Filename: ip_info.py
# claudia
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "9/12/21"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import urllib.request
import ssl
import json


def main():
    """
    Python only script to obtain location information for a give IP address
    :return:
    """

    # Define a context to disable hostname and SSL Certificate verification
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://ipapi.co/json/"

    if arguments.interactive:
        ip = input("Enter IP to Lookup: ")
        url = f"https://ipapi.co/{ip.strip()}/json/"
    elif arguments.address:
        url = f"https://ipapi.co/{arguments.address.strip()}/json/"


    # urllib returns byte string
    contents_bytes = urllib.request.urlopen(url, context=ctx).read()
    print(f"\n---- Raw Response:\n{contents_bytes}")
    print(type(contents_bytes))

    # decode byte string into string and use json module to load into a dictionary structure
    contents = json.loads(contents_bytes.decode())
    print(f"\n--- Response converted to Python Dictionary:\n{contents}")
    # print(type(contents))

    # Use json module to load contents, now a string, into a dictionary structure
    contents_dict = dict(contents)
    print(f"\nResponse for ip {contents_dict['ip']}:\n{json.dumps(contents_dict, indent=4)}")
    print(type(contents))

    ip_file_name = f"ip_info.json"

    print(f"\nLocation of IP ({contents_dict['version']}) {contents_dict['ip']}: {contents_dict['city']}, {contents_dict['region']} {contents_dict['country_name']}\n")


    with open(ip_file_name, "w") as json_file:
        json.dump(contents, json_file, indent=4)

    print(f"\nSaved ipapi.co API response in JSON file {ip_file_name}\n")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python ip_info.py' ")
    parser.add_argument('-i', '--interactive', help='Interactively ask for the IP Address via CLI',
                        action='store_true', default=False)
    parser.add_argument('-a', '--address', help='Provide address', action='store',
                        default=False)
    arguments = parser.parse_args()
    main()
