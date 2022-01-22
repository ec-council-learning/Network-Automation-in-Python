#!/usr/bin/env python3

import argparse
# TODO: Add any additional required modules
import netmiko
import getpass
import os


# TODO: Think about reusability
def my_function():
    pass

def get_creds_interactive():
    uname = input("Enter Username: ")
    pwd = getpass.getpass("Enter Password: ")
    sec = getpass.getpass("Enter Secret: ")

    return uname, pwd, sec


def main():

    """
    This script utilizes Netmiko to log in to one or more devices, 	
    executes one or more show commands, 
    and stores the output to a list of lists
    """

    # Define list of network devices for the script to access
    dev_list = ["10.1.10.54", "10.1.10.55"]

    # Set TextFSM environment variable for parsing show command output (Future)

    NET_TEXTFSM=os.path.join(os.path.expanduser("~"),"ntc-templates","ntc_templates" ,"templates")
    os.environ["NET_TEXTFSM"] = NET_TEXTFSM

    # Define list of show commands to execute against each network device
    show_cmds = [
        "show version",
        "show inventory",
        "show run",
    ]

    # Define a main list to hold all output across all devices
    all_dev_output_list = []

    username, password, secret = get_creds_interactive()

    # Loop over devices
    for dev in dev_list:

        # Create device dictionaries for each device 
        # REFACTOR Add credentials managment so credentials are not hardcoded
        dev_dict = {
            'device_type': 'arista_eos',
            'host':   dev,
            'username': username,
            'password': password,
            'port' : 22,          
            'secret': secret,   
            'verbose': False,
        }

        # Create a temporary list which is re-initialized at the start of processing a new device to hold the device and all the output
        # REFACTOR Change to a dictionary so that its easier to get to the information
        tmp_dict = dict()

        # Initialize the Connection Object to the device
        dev_conn_obj = netmiko.ConnectHandler(**dev_dict)

        tmp_dict.update({"device": dev})
        # Loop over show commands and concatenate output into a string
        for cmd in show_cmds:   
            print(cmd)
            tmp_dict.update({cmd: dev_conn_obj.send_command(cmd, use_textfsm=True)})

        # Save device id and concatenated show command output to the temporary list creating a list with two elements, the first is the device, and the second is the show command output string for that device

        # Append temporary list to main list creating a list of dictionaries
        all_dev_output_list.append(tmp_dict)

        # Close connection to device
        dev_conn_obj.disconnect()

    for line in all_dev_output_list:
        print(line['device'])
        #print(line['show version'])
        print(line['show version'][0]['image'])
        print("-------")
    print(len(all_dev_output_list))
    

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
