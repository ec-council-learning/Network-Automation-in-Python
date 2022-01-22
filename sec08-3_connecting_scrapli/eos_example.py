#!/usr/bin/env python3

import argparse
# Add any additional required modules
import scrapli
import getpass
import json
import os


def get_creds_interactive(get_secret=False):
    """
    Function to interactively query for network device credentials
    :param get_secret: Optional argument to query for enable or secret. Defaults to False and sec set to pwd.
    :return: uname, pwd, sec
    """
    uname = input("Enter Username: ")
    pwd = getpass.getpass("Enter Password: ")
    # TODO: Add option to bypass asking for enable or secret password if not needed
    if get_secret:
        sec = getpass.getpass("Enter Secret: ")
    else:
        sec = pwd
    return uname, pwd, sec


def main():
    """
    This script will connect to a network device using the Scrapli Core EOS Driver
    """

    # Define list of network devices for the script to access
    # by default define the hardcoded list
    dev_list = ["10.1.10.54", "10.1.10.55"]

    # TODO: Add option to provide text file of IPs or FQDNs
    # If the -f optional command line option was used build list from the given file and overwrite dev_list
    if arguments.file_of_devices:
        # Check to make sure the file exists
        if os.path.exists(arguments.file_of_devices):
            with open(arguments.file_of_devices, 'r') as fh:
                dev_list = fh.readlines()
                print(f"Using Devices from file {arguments.file_of_devices}\n{dev_list}")
        else:
            print(f"ERROR! File provided via command line does not exist.  Using hardcoded device list.\n{dev_list}")


    # Define list of show commands to execute against each network device
    show_cmds = [
        "show version",
        "show inventory",
        "show ip interface brief",
    ]

    # Assumes all devices use same credential (otherwise move into for loop so creds are prompted for each device)
    username, password, secret = get_creds_interactive()

    # Initialize a list to hold all the results
    all_dev_output_list_of_dicts = []

    for dev in dev_list:

        # (RE) Initialize a temporary dictionary to hold the results for each device
        tmp_dict = dict()
        tmp_dict.update({"device" : dev})
        # Create device dictionaries for each device
        dev_dict = {
            "host": dev,
            "auth_username": username,
            "auth_password": password,
            "auth_secondary": secret,
            "auth_strict_key": False,
            "port": 22,
        }

        # Note the use of Python's Context Manager ("with") to handle opening and closing of the connection
        with scrapli.driver.core.EOSDriver(**dev_dict) as conn:
            for cmd in show_cmds:
                print(f"\n==== Sending show command {cmd} to device {dev} ====")
                result = conn.send_command(cmd)
                print(result.result)
                parsed_result = result.textfsm_parse_output()
                print(parsed_result)

                tmp_dict.update({cmd : parsed_result})

        all_dev_output_list_of_dicts.append(tmp_dict)

    # TODO: Update script to save the data to a JSON file
    output_filename = f"{os.path.basename(__file__)}_all_output.json"
    with open(output_filename, "w") as fh:
        json.dump(all_dev_output_list_of_dicts, fh, indent=4)

    print(f"\n---- All Output Saved to JSON file:\n{os.path.join(os.getcwd(), output_filename)}\n")

    if arguments.verbose:
        print(f"\nScript Arguments via Command Line at Execution are:\n{arguments}\n")


# Standard call to the main() function.
if __name__ == '__main__':

    # Initialize the Argument Parser object and include a description of the script and a hint on how touse
    parser = argparse.ArgumentParser(
        description="Fill in a short Script Description",
        epilog="Usage: ' python eos_exammple.py -v -f my_ip_file.txt' ",
    )
    
    # Add the first required positional argument (Example)
    # parser.add_argument("first_argument", type=str, help="First argument, string type")
    
    # Add an optional argument - Boolean so including the option sets "verbose" to True, Fase is the default
    parser.add_argument("-v", "--verbose",  action="store_true", help="Print Command Line Arguments passed to script", default=False)

    # Option to provide a text file with IPs or FQDNs of network devices
    parser.add_argument("-f", "--file_of_devices",  action="store", help="Optional local text file containing one IP or FQDN per line")

    arguments = parser.parse_args()

    main()

