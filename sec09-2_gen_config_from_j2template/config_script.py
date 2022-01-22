#!/usr/bin/env python3

import argparse
# TODO: Add any additional required modules
import jinja2
import os
import datetime


# TODO: Think about reusability
def save_to_text_file(fn, data):
    with open(fn, "w") as cfgfile:
        cfgfile.write(data)
    print(f"\nSaved Rendered Configuration to file {fn} in current script directory.")


def main():
    """
    This script will create a configuration from a Jinja2 template using hardcoded data and save it to a text file
    """

    # TODO: Define the Template to be used in this script which resides in the j2templates subfolder
    j2template = "vlans.j2"

    # TODO: Create the Jinja2 Environment using a subfolder called "j2templates"
    j2template_folder_path = os.path.join(os.getcwd(), "j2templates")

    print(f"Creating Jinja2 Template Environment for templats in {j2template_folder_path}")
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(j2template_folder_path))

    # TODO: Create the Template object we will use to render from the specific template we want to use
    print(f"Creating the Template object using template {j2template}")
    template = template_env.get_template(j2template)

    # Data
    # TODO: Define a timestamp variable to use so we know when the config was generated
    dattim = format(datetime.datetime.now())

    # TODO: Create the data structure which will be sent for rendering
    data_list_of_dicts = [
        {"99": "Badge_Reader_Vlan"},
        {"100": "Printer_Vlan"},
        {"200": "General_Use_Vlan"},
        {"999": "Guest_Vlan"},
    ]

    # TODO: Render
    rendered = template.render(gen_time=dattim, data_list_of_dicts=data_list_of_dicts)
    # TODO: Add device name to template

    # TODO: Save the rendered configuration to a file
    # TODO: Add template to filename
    cfg_filename = f"{arguments.device_name}_config.txt"
    save_to_text_file(cfg_filename, rendered)

    if arguments.verbose:
        print(f"\nScript Arguments via Command Line at Execution are:\n{arguments}\n")


# Standard call to the main() function.
if __name__ == '__main__':

    # Initialize the Argument Parser object and include a description of the script and a hint on how touse
    parser = argparse.ArgumentParser(
        description="Fill in a short Script Description",
        epilog="Usage: ' python config_script.py device_name' ",
    )
    
    # Add the first required positional argument (Example)
    parser.add_argument("device_name", type=str, help="Device name for rendered configuration")
    
    # Add an optional argument - Boolean so including the option sets "verbose" to True, Fase is the default
    parser.add_argument("-v", "--verbose",  action="store_true", default=False)

    arguments = parser.parse_args()

    main()
