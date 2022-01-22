#!/usr/bin/env python3

import argparse
# TODO: Add any additional required modules
import scrapli
import getpass
import json
import os


def get_creds_interactive(get_secret=False):
    uname = input("Enter Username: ")
    pwd = getpass.getpass("Enter Password: ")
    if get_secret:
        sec = getpass.getpass("Enter Secret: ")
    else:
        sec = pwd

    return uname, pwd, sec


def main():
    """
    This script will connect to a network device using the Scrapli Generic Driver
    """

    # Define list of network devices for the script to access
    dev_list = ["10.1.10.61", "10.1.10.61"]

    # Define list of show commands to execute against each network device (VyOS commands)
    show_cmds = [
        "show version",
        "show interfaces",
        "show configuration",
    ]

    # Assumes all devices use same credential (otherwise move into for loop so creds are prompted for each device)
    username, password, secret = get_creds_interactive()

    all_dev_output_list_of_dicts = []
    for dev in dev_list:

        tmp_dict = dict()
        tmp_dict.update({"device" : dev})
        # Create device dictionaries for each device
        dev_dict = {
            "host": dev,
            "auth_username": username,
            "auth_password": password,
            # "auth_secondary": secret,
            "auth_strict_key": False,
            "port": 22,
        }

        # The `GenericDriver` is a good place to start if your platform is not supported by a "core"
        #  platform driver
        conn = scrapli.driver.GenericDriver(**dev_dict)
        conn.open()

        print(conn.channel.get_prompt())

        # IMPORTANT: paging is NOT disabled w/ GenericDriver driver!
        conn.send_command("terminal length 0")

        for cmd in show_cmds:
            print(f"\n==== Sending show command {cmd} to device {dev} ====")
            result = conn.send_command(cmd)
            print(f"---- Raw Results:\n{result.result}\n")
            parsed_result = result.textfsm_parse_output()
            print(f"---- Parsed Results:\n{parsed_result}\n")

            # Check for parsed results
            if parsed_result:
                tmp_dict.update({cmd : parsed_result})
            else:
                tmp_dict.update({cmd: result.result})

        all_dev_output_list_of_dicts.append(tmp_dict)

        conn.close()

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
        epilog="Usage: ' python script-name script arguments' ",
    )
    
    # Add the first required positional argument (Example)
    # parser.add_argument("first_argument", type=str, help="First argument, string type")
    
    # Add an optional argument - Boolean so including the option sets "verbose" to True, Fase is the default
    parser.add_argument("-v", "--verbose",  action="store_true", default=False)

    arguments = parser.parse_args()

    main()

