#!/usr/bin/env python3

import sys

def my_function():
    pass


def main():
    """
    This script ...
    """

    # Open the text file containing the output of show version
    # Read in the output
    # Turn the output into a list so we can check each line
    file_name = "iosxe_show_version.txt"
    with open(file_name) as file:
        data_list = file.readlines()
    # Search each line for the information we want
    # Save each piece of information to a variable
    for line in data_list:
        if "uptime" in line:
            tmp_list = line.split(" ")
            hostname = tmp_list[0]

        if "Cisco IOS Software" in line:
            tmp_list  = line.split(",")
            version = tmp_list[2]

    # Display the information to our screen
    print(f"\nDevice {hostname} is running version {version}\n")

# Standard call to the main() function.
if __name__ == '__main__':
    print(f"List of command line arguments passed to the script.\n{sys.argv}\nThe first element is always the script name.")
    main()
