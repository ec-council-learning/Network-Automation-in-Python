#!/usr/bin/env python3

import argparse
# TODO: Add any additional required modules


# TODO: Think about reusability
def my_function():
    pass


def main():
    """
    This script ...
    """
    
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
