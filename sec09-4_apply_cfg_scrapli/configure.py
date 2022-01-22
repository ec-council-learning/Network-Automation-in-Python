#!/usr/bin/env python3

import argparse
import getpass
import jinja2
import datetime
import scrapli
import yaml
import os


# From Section 8.3
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


# From Section 9.2
def save_to_text_file(fn, data):
    with open(fn, "w") as cfgfile:
        cfgfile.write(data)
    print(f"\nSaved Rendered Configuration to file {fn} in current script directory.")


# From Section 9.2 - Create configuration from a Jinja2 Template - Converted to a function
def render_j2(j2template_filename, template_data_dict, view_rendered=False):

    j2template_folder_path = os.path.join(os.getcwd(), "j2templates")

    print(
        f"Creating Jinja2 Template Environment for templates in {j2template_folder_path}"
    )
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(j2template_folder_path)
    )

    # Create the Template object we will use to render from the specific template we want to use
    print(f"Creating the Template object using template {j2template_filename}")
    template = template_env.get_template(j2template_filename)

    # Data -  All data has been passed to this function in the template_data_dict variable

    # Render
    rendered_cfg = template.render(data_dict=template_data_dict)

    if view_rendered:
        print(f"\nRendered Result:\n{rendered_cfg}")

    return rendered_cfg


# From Section 5.3 - Converted to a function
def get_host_info(host_file="hosts.yml"):

    # Initialize inventory dict in case something goes wrong in open block.
    inv_dict = {}
    with open(host_file) as f:
        inv_dict = yaml.full_load(f)
    print(f"\nInventory dictionary from host file {host_file}: \n{inv_dict}\n")
    return inv_dict


def scrapli_send_cfg_file(conn_obj, cfg_file, save_cfg=False):
    """
    Configure a device vith a list of configuration commands
    :param conn_obj: Scrapli Connection Object (Established SSH session to a specific device)
    :param cmd_list: list of commands to send
    :param save_cfg: Optional boolean to save updated configuration. Defaults to false.
    :return:
    """

    results = conn_obj.send_configs_from_file(cfg_file, stop_on_failed=True)
    print(results.result)

    if save_cfg:
        save_results = conn_obj.send_command("write mem")
        print(f"Configuration has been saved!\n{save_results}\n{save_results.result}")
    else:
        print("Alert! Configuration has not been saved!")

    print(f"Returning results {results} for host {results.host}")

    # If the config push failed in some way, print warning and the results result text
    if results.failed:
        print(f"WARNING - Problem with configuration")
        print(results.result)

    return results


# From Section 8 - Converted to a function
def create_dev_dict(dev_info_dict):

    username, password, secret = get_creds_interactive()
    dev_dict = {
        "host": dev_info_dict["hostname"],
        "auth_username": username,
        "auth_password": password,
        "auth_secondary": secret,
        "auth_strict_key": False,
        "port": 22,
    }
    return dev_dict


def main():
    """
    This script will generate a configuration snippet, save to a file, and apply the configuration to a network device.
    A text file of IPs or FQDNs must be provided as a required parameter for the script to execute.
    """

    # Read in list of devices from file .. assume file is named hosts.yml
    all_devs_dict = get_host_info(arguments.hosts_file)

    # Iterate over each device in the YAML hosts file
    for dev in all_devs_dict.keys():
        print(f"\n===== Configuring Device {dev} =====")

        # Build Template Data (Payload)
        # This dictionary will hold all the data needed to generate a device specific configuration snippet
        data_dict = {}

        # TODO: Remove configuration payload from script
        data_lod = [
            {"99": "Badge_Reader_Vlan"},
            {"100": "Printer_Vlan"},
            {"200": "General_Use_Vlan"},
            {"300": "Wireless_Vlan"},
            {"999": "Guest_Vlan"},
        ]

        data_dict.update({"device": dev})

        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%d %b, %Y %H:%M:%S %p")
        data_dict.update({"timestamp": timestamp})

        data_dict.update({"data_list_of_dicts": data_lod})

        # Create Templating Environment and Render
        j2template = "vlans.j2"
        rendered = render_j2(j2template, data_dict, view_rendered=False)

        # Save Configuration Snippet
        cfg_filename = f"{dev}_config.txt"
        save_to_text_file(cfg_filename, rendered)

        # Create device dictionary for device
        dev_dict = create_dev_dict(all_devs_dict[dev])

        # Establish Connection to Device
        # Note the use of Python's Context Manager ("with") to handle opening and closing of the connection
        with scrapli.driver.core.EOSDriver(**dev_dict) as conn:

            # Note: while we saved the configuration snippet, we have it in memory in the rendered variable
            # but to use will require some processing (turn into a list) so using Scraplis send_configs_from_file
            scrapli_send_cfg_file(conn, cfg_filename, save_cfg=arguments.save_config)


# Standard call to the main() function.
if __name__ == "__main__":

    # Initialize the Argument Parser object and include a description of the script and a hint on how touse
    parser = argparse.ArgumentParser(
        description="Script to send configuration commands generated realtime to one or more network devices listed in hosts.yml file by default",
        epilog="Usage: ' python configure.py' ",
    )

    # Add the first required positional argument (Example)
    parser.add_argument(
        "-f",
        "--hosts_file",
        type=str,
        action="store",
        default="hosts.yml",
        help="Name of YAML Host file with devices. Default is hosts.yml",
    )

    parser.add_argument(
        "-s",
        "--save_config",
        action="store_true",
        default=False,
        help="Use -s in the CLI to save the configuration. By default the configuration on the device is not saved",
    )

    arguments = parser.parse_args()

    main()
