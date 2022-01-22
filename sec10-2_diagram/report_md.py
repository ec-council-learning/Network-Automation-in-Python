#!/usr/bin/env python3

import argparse
import getpass
import os
import netmiko
import jinja2
import yaml
import pprint
import datetime
from nwdiag import parser, builder, drawer


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
    NET_TEXTFSM=os.path.join(os.path.expanduser("~"),"ntc-templates","ntc_templates","templates")
    os.environ["NET_TEXTFSM"] = NET_TEXTFSM

    # Read in list of devices from file .. assume file is named hosts.yml
    all_devs_dict = get_host_info(arguments.hosts_file)

    # Lab Network Diagram Payload
    net_diagram = """
    nwdiag {
      External_Network [shape = cloud];
      External_Network -- Management;
      network Management {
          address = "10.1.10/24"

          sw01 [address = "10.1.10.54"];
          sw02 [address = "10.1.10.55"];
      }
    }
    """

    # Generate Lab Topology
    tree = parser.parse_string(net_diagram)
    diagram = builder.ScreenNodeBuilder.build(tree)
    draw = drawer.DiagramDraw('PNG', diagram, filename="network_topology.png")
    draw.draw()
    draw.save()

    # For Each Device:
    # - Define data structure to save all output results
    # - Create a device dictionary for each device
    # - Establish SSH connection to the device
    # - Snapshot the vlan configuration of the device
    # - Generate As Built Report (Text Report) and save to file which includes the device name

    # Set Current time for text friendly timestamp and file timestamp
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%d %b, %Y %H:%M:%S %p")

    # Define data structure to save all output results
    # Initialize dictionary to save all output
    # Reminder: Jinja2 Template is looking for keys of device, timestamp, pre_vlan_cfg, cfg_cmd_list,
    # post_vlan_cfg, cfg_response
    cfg_record_dict = {}
    cfg_record_dict.update({"timestamp": timestamp})
    cfg_record_dict.update({"devices": {}})

    # Iterate over each device in the YAML hosts file
    for dev in all_devs_dict.keys():
        print(f"\n===== Configuring Device {dev} =====")
        tmp_record_dict = dict()
        tmp_record_dict.update({"device": dev})

        # Create device dictionary for device
        dev_dict = create_dev_dict(all_devs_dict[dev])

        # Initialize the Connection Object to the device
        dev_conn_obj = netmiko.ConnectHandler(**dev_dict)

        # Snapshot the current (pre-change) vlan configuration of the device
        cmd = "show vlan"
        vlan_snapshot = dev_conn_obj.send_command(cmd, use_textfsm=True)
        # vlan_snapshot is a list of dictionaries
        # In the report a list of lists will look better so lets convert the list of dicts to a list of lists
        vlan_snapshot_list = []
        header = list(vlan_snapshot[0].keys())
        tmp_record_dict.update({"vlan_header": header})
        for line in vlan_snapshot:
            vlan_snapshot_list.append(list(line.values()))

        tmp_record_dict.update({"vlan_cfg": vlan_snapshot_list})
        print("-- Pre Change Snapshot - Parsed show vlan")
        print(pprint.pprint(vlan_snapshot_list))

        # Close connection to device
        dev_conn_obj.disconnect()

        cfg_record_dict['devices'].update({dev: tmp_record_dict})

    # Generate report
    j2template = "as_built_md.j2"
    rendered = render_j2(j2template, cfg_record_dict, view_rendered=False)

    # Save rendered report to file
    report_filename = f"Vlan_Configuration_Report_ASBUILT_{current_time.strftime('%Y-%m-%d')}.md"
    save_to_text_file(report_filename, rendered)


# Standard call to the main() function.
if __name__ == '__main__':

    # Initialize the Argument Parser object and include a description of the script and a hint on how touse
    argparser = argparse.ArgumentParser(
        description="Script to send configuration commands generated realtime to one or more network devices listed in hosts.yml file by default and generate report",
        epilog="Usage: ' python as_built.py' ",
    )

    # Add the first required positional argument (Example)
    argparser.add_argument(
        "-f",
        "--hosts_file",
        type=str,
        action="store",
        default="hosts.yml",
        help="Name of YAML Host file with devices. Default is hosts.yml",
    )

    argparser.add_argument(
        "-c",
        "--cfg_payload_file",
        type=str,
        action="store",
        default="cfg_payload.yml",
        help="Name of YAML file with Vlan configuration. Default is cfg_payload.yml",
    )

    argparser.add_argument(
        "-s",
        "--save_config",
        action="store_true",
        default=False,
        help="Use -s in the CLI to save the configuration. By default the configuration on the device is not saved",
    )

    arguments = argparser.parse_args()

    main()
