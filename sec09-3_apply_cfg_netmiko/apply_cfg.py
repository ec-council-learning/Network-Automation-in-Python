#!/usr/bin/env python3

import argparse
import getpass
import netmiko
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


def netmiko_send_cfg_list(conn_obj, cfg_file, save_cfg=False):
    """
    Configure a device vith a list of configuration commands read from a file
    :param conn_obj: Netmiko Connection Object (Established SSH session to a specific device)
    :param cfg_file: text file with configuration
    :param save_cfg: Optional boolean to save updated configuration. Defaults to false.
    :return:
    """

    # Check to make sure the file exists
    if os.path.exists(cfg_file):
        # Open configuration file and read in each line
        with open(cfg_file) as fh:
            cmd_list = fh.readlines()

        results = conn_obj.send_config_set(cmd_list)

    if save_cfg:
        results += conn_obj.send_command("write mem")
        print(f"Configuration has been saved!\n{results}")
    else:
        print("Alert! Configuration has not been saved!")

    return results


def netmiko_send_cfg_file(conn_obj, cfg_file, save_cfg=False):

    # Initialize results in case the file exists test fails since the function returns the results value.
    results = ""

    # Check to make sure the file exists
    if os.path.exists(cfg_file):

        # Notice Netmmiko handles opening the file for us!
        results = conn_obj.send_config_from_file(cfg_file)

        if save_cfg:
            results += conn_obj.save_config()
            print(f"Configuration has been saved!\n{results}")
        else:
            print("Alert! Configuration has not been saved!")

    return results


def main():
    """
    This script will apply the commands found in a configuration file to a device.
    Both the device FQDN or IP and the config text file must be provided vi the command line.
    """

    # Establish Connection to Device
    username, password, secret = get_creds_interactive()
    dev_dict = {
        "device_type": "arista_eos",
        "host": arguments.device,
        "username": username,
        "password": password,
        "port": 22,
        "secret": secret,
        "verbose": True,
    }

    # Initialize the Connection Object to the device
    dev_conn_obj = netmiko.ConnectHandler(**dev_dict)

    # Send a list of configuration commands
    netmiko_send_cfg_list(
        dev_conn_obj, arguments.cfg_file, save_cfg=arguments.save_config
    )

    # Send commands from a file
    # res = netmiko_send_cfg_file(dev_conn_obj, arguments.cfg_file, save_cfg=arguments.save_config)
    print(res)

    dev_conn_obj.disconnect()


# Standard call to the main() function.
if __name__ == "__main__":

    # Initialize the Argument Parser object and include a description of the script and a hint on how touse
    parser = argparse.ArgumentParser(
        description="Script to send configuration commands in a file to a network device.",
        epilog="Usage: ' python apply_cfg.py switch config_file' ",
    )

    # Add required positional arguments
    parser.add_argument("device", type=str, help="Device name or IP")
    parser.add_argument("cfg_file", type=str, help="Configuration File to Apply")

    # Add optional command line arguments
    parser.add_argument(
        "-s",
        "--save_config",
        action="store_true",
        help="Use -s in the CLI to save the configuration. By default the configuration on the device is not saved",
        default=False,
    )

    arguments = parser.parse_args()

    main()
