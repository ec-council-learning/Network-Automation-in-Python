#!/usr/bin/env python3

import argparse
import getpass
import os
import netmiko
import jinja2
import yaml
import pprint
import datetime


# From Section 6.2 Credentials
def set_creds_env(verbose=False):
    """
    Function queries user for network credentials and sets environment variables USERNAME, PASSWORD, SECRET
    :param verbose: Optional boolean for verbose output. Default is False.
    :return: creds_dict: Credentials Dictionary with keys username, password, and secret
    """

    # Interactive input of credentials
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    # Populate credentials dictionary
    # By convention Environment Variables are all UPPERCASE
    creds_dict = {
        "USERNAME": username.strip(),
        "PASSWORD": password.strip(),
        "SECRET": password.strip()
    }

    for cred in creds_dict.keys():
        # Set each environment variable
        print(f"\n==== Setting Environment Variable {cred}")
        os.environ[cred] = creds_dict[cred]

        if verbose:
            print(f"Checking for {cred}...")
            cred_value = os.getenv(cred)
            print(f"Environment Variable {cred} has value {cred_value}\n")

    return creds_dict


# From Section 8 - Converted to a function
def create_dev_dict(dev_info_dict):
    """
    Function to create a device dictionary to use in establishing a Netmiko connection
    :param dev_info_dict: specific device dictionary including FQDN or IP and device type
    :return: dev_dict: device dictionary to use with Netmiko
    """

    dev_dict = {
        "device_type": dev_info_dict['device_type'],
        "host": dev_info_dict['hostname'],
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "port": 22,
        "secret": os.getenv("SECRET"),
        "verbose": True,
    }

    return dev_dict


# From Section 9.2
def save_to_text_file(fn, data):
    with open(fn, "w") as cfgfile:
        cfgfile.write(data)
    print(f"\nSaved Rendered Configuration to file {fn} in current script directory.")


# From Section 5.3 - Converted to a function
def get_host_info(host_file="hosts.yml"):
    # Initialize inventory dict in case something goes wrong in open block.
    inv_dict = {}
    with open(host_file) as f:
        inv_dict = yaml.full_load(f)
    print(f"\nInventory dictionary from host file {host_file}: \n{inv_dict}\n")
    return inv_dict


# From Sections 5.3 and 9.4
def load_yaml_file(cfg_payload_file="cfg_payload.yml"):
    # Initialize inventory dict in case something goes wrong in open block.
    cfg_data_dict = {}
    with open(cfg_payload_file) as f:
        cfg_data_dict = yaml.full_load(f)
    print(f"\nConfiguration Data Loaded from file {cfg_payload_file}: \n{cfg_data_dict}\n")
    return cfg_data_dict


# From Section 9.3 - Modified to take a list of commands
def netmiko_send_cfg_list(conn_obj, cmd_list, save_cfg=False):
    """
    Configure a device vith a list of configuration commands read from a file
    :param conn_obj: Netmiko Connection Object (Established SSH session to a specific device)
    :param cfg_cmd_list: text file with configuration
    :param save_cfg: Optional boolean to save updated configuration. Defaults to false.
    :return:
    """

    results = conn_obj.send_config_set(cmd_list)

    if save_cfg:
        results += conn_obj.send_command("write mem")
        print(f"Configuration has been saved!\n{results}")
    else:
        print("Alert! Configuration has not been saved!")

    return results


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


def main():
    """
    This script sends a list of configuration commands loaded from a
    configuration YAML file which by default is named cfg_payload.yml
    to each device listed in a YAML hosts file which by default is named hosts.yml
    and saved the change to each device in a report for each device.
    """

    # Set Credentials as Environment Variables
    set_creds_env(verbose=True)

    # Set TextFSM environment variable for parsing show command output (Future)
    NET_TEXTFSM=os.path.join(os.path.expanduser("~"),"ntc-templates","ntc_templates" ,"templates")
    os.environ["NET_TEXTFSM"] = NET_TEXTFSM

    # Read in list of devices from file .. assume file is named hosts.yml
    all_devs_dict = get_host_info(arguments.hosts_file)

    # For Each Device:
    # - Define data structure to save all output results
    # - Generate the list of config commands
    # - Create a device dictionary for each device
    # - Establish SSH connection to the device
    # - Snapshot the current (pre-change) vlan configuration of the device
    # - Send configuration commands to the device
    # - Snapshot the new (post-change) vlan configuration of the device
    # - Generate As Built Report (Text Report) and save to file which includes the device name

    # Iterate over each device in the YAML hosts file
    for dev in all_devs_dict.keys():
        print(f"\n===== Configuring Device {dev} =====")

        # Define data structure to save all output results
        # Initialize dictionary to save all output
        # Reminder: Jinja2 Template is looking for keys of device, timestamp, pre_vlan_cfg, cfg_cmd_list,
        # post_vlan_cfg, cfg_response
        cfg_record_dict = {}
        cfg_record_dict.update({"device": dev})

        # Load configuration data from YAML file
        data_lod = load_yaml_file()
        print(pprint.pprint(data_lod))

        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%d %b, %Y %H:%M:%S %p")
        cfg_record_dict.update({"timestamp": timestamp})

        # Create device dictionary for device
        dev_dict = create_dev_dict(all_devs_dict[dev])

        # Initialize the Connection Object to the device
        dev_conn_obj = netmiko.ConnectHandler(**dev_dict)

        # Snapshot the current (pre-change) vlan configuration of the device
        cmd = "show vlan"
        pre_vlan_snapshot = dev_conn_obj.send_command(cmd, use_textfsm=False)
        # Save the PRE vlan snapshot (parsed) to the cfg_record_dict
        cfg_record_dict.update({"pre_vlan_cfg": pre_vlan_snapshot})
        print("-- Pre Change Snapshot - Parsed show vlan")
        print(pprint.pprint(pre_vlan_snapshot))

        # Send a list of configuration commands
        # Create the list of commands on the fly from the loaded YAML payload
        cmd_list = []
        for line in data_lod:
            cmd_list.append(f"vlan {line['vlan_id']}")
            cmd_list.append(f" name {line['vlan_name']}")
        # Save the list of configuration commands we are sending to the device to the cfg_record_dict
        cfg_record_dict.update({"cfg_cmd_list": cmd_list})
        print(f"-- Configuration Command List to send to {dev}")
        print(pprint.pprint(cmd_list))

        # Send configuration commands to device
        cfg_response = netmiko_send_cfg_list(
            dev_conn_obj, cmd_list, save_cfg=arguments.save_config
            )
        # Save the device output
        cfg_record_dict.update({"cfg_response": cfg_response})

        # Snapshot the resulting (post-change) vlan configuration of the device
        post_vlan_snapshot = dev_conn_obj.send_command(cmd, use_textfsm=False)
        # Save the POST vlan snapshot (parsed) to the cfg_record_dict
        cfg_record_dict.update({"post_vlan_cfg": post_vlan_snapshot})
        print("-- Pre Change Snapshot - Parsed show vlan")
        print(pprint.pprint(pre_vlan_snapshot))

        # Close connection to device
        dev_conn_obj.disconnect()

        # Generate report
        j2template = "as_built.j2"
        rendered = render_j2(j2template, cfg_record_dict, view_rendered=False)

        # Save rendered report to file
        report_filename = f"{dev}_Vlan_Configuration_Report_ASBUILT.txt"
        save_to_text_file(report_filename, rendered)


# Standard call to the main() function.
if __name__ == '__main__':

    # Initialize the Argument Parser object and include a description of the script and a hint on how touse
    parser = argparse.ArgumentParser(
        description="Script to send configuration commands generated realtime to one or more network devices listed in hosts.yml file by default and generate report",
        epilog="Usage: ' python as_built.py' ",
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
        "-c",
        "--cfg_payload_file",
        type=str,
        action="store",
        default="cfg_payload.yml",
        help="Name of YAML file with Vlan configuration. Default is cfg_payload.yml",
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
