#!/usr/bin/env python3

import sys
import yaml
import pythonping
import json

def my_function():
    pass


def main():
    """
    This script will read in a YAML inventory file and ping the devices
    """

    hfile = "hosts.yml"
    with open(hfile) as f:
      inv_dict = yaml.full_load(f)
    print(f"\nInventory dictionary: \n{inv_dict}\n")

    print(json.dumps(inv_dict, indent=4))

    print(f"\nKeys: {inv_dict.keys()}")
    print(f"\nValues: {inv_dict.values()}\n")

    for dev, dev_info_dict in inv_dict.items():
      print(f"\n==== Device {dev}")
      print(f"\t{json.dumps(dev_info_dict, indent=4)}")
      result = pythonping.ping(dev_info_dict['hostname'], verbose=True)




# Standard call to the main() function.
if __name__ == '__main__':
    print(f"List of command line arguments passed to the script.\n{sys.argv}\nThe first element is always the script name.")
    main()
