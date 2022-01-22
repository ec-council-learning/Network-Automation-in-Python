import sys
from datetime import datetime
from icecream import ic 


def prefix(msg):
    return f'{msg}|> '


def print_header(title, width=60, delimeter= "="):
    title_len = len(title)
    space_left = width - title_len

    if space_left > 0:
        num_delim = int(space_left/2)

    formatted_title = f"{delimeter*num_delim} {title} {delimeter*num_delim}"

    print()
    print(delimeter*len(formatted_title))
    print(f"{delimeter*num_delim} {title} {delimeter*num_delim}" )
    print(delimeter*len(formatted_title))
    print()


def continue_or_exit():
    cont = input("\nDo You Want To Continue? (any key or n) \n").strip()
    if cont == "n":
        sys.exit()      


def main():

    ic.configureOutput(prefix=prefix("Python Reminders"), includeContext=True)

    print_header("Variables & Assignments")
    # Variables  & Assignments

    print("Variables are case sensitive!  maxBandwidth does not equal maxbandwidth")
    print("Variables can have letters, numbers, and undercores _ but cannot begin with a number")
    print("Classes use fist letter upper case convention")

    # ERROR! Not a Valid variable name
    # 6issix = 6
    # max-bandwidth = 100

    sixis6 = 6
    # Camel case or Snake Case is valid
    ic.configureOutput(prefix=prefix("camelCase"), includeContext=True)
    camelCase = "Can be shorter"
    ic(camelCase)

    ic.configureOutput(prefix=prefix("snake_case"), includeContext=True)
    snake_case = "Can be longer"
    ic(snake_case)

    continue_or_exit()

    print_header("Integers & Floating Point", delimeter="-")
    # Integers & Floating point
    ic.configureOutput(prefix=prefix("Integer"), includeContext=True)
    total_cfg_files = 1

    print(f"total_cfg_files = {total_cfg_files}")
    print({type(total_cfg_files)})

    ic(total_cfg_files)
    ic(type(total_cfg_files))

    continue_or_exit()

    num_devices = 2
    maxBandwidth = 150.7

    ic(num_devices)
    ic(type(num_devices))

    ic.configureOutput(prefix=prefix("Floating Point"), includeContext=True)

    ic(maxBandwidth)
    ic(type(maxBandwidth))

    # Python tries to do what makes senses
    print("\nMultiplying integer and float:")
    ic(maxBandwidth * num_devices)
    ic(type(maxBandwidth * num_devices))
    print("\nAdding integer and float:")
    ic(maxBandwidth + num_devices)
    ic(type(maxBandwidth + num_devices))

    continue_or_exit()

    print_header("Booleans (True or False)", delimeter="-")
    ic.configureOutput(prefix=prefix("Booleans"), includeContext=True)
    # Booleans
    ic(total_cfg_files)

    files_exist = False
    ic(files_exist)

    if total_cfg_files == 1:
        print(f"\nWe have at least one file if total_cfg_files == 1!")
        files_exist = True
    ic(files_exist)
    ic(type(files_exist))

    if files_exist:
        print(f'\nWe have "at least" one file if file_exists is True!')

    continue_or_exit()

    print_header("Strings", delimeter="-")
    ic.configureOutput(prefix=prefix("Strings"), includeContext=True)
    # String
    # Can be quoted with ""
    # Can be quoted with ''
    cfg_filename1 = "retail-rtr.txt"
    cfg_filename2 = 'csr1000v-1.txt'
    ic(cfg_filename1)
    ic(type(cfg_filename1))
    ic(cfg_filename2)
    ic(type(cfg_filename2))

    mac_text = """
    0057.d21b.7d00
    0057.d21b.7d00
    a4bb.6da1.68e4
    0008.6600.2ae4
    0003.5b0a.2bdd
    0003.5b0a.2bdc
    0003.5b0a.2bdc
    509a.4c48.3214
    484d.7ee4.9ccb
    484d.7edc.e24b
    1866.da3b.99e1
    1866.da3b.a40a
    6012.8bd3.1d8f
    b07b.2540.514c
    509a.4c48.2cce
    509a.4c48.2cce
    00a7.42f6.b434
    """

    ic(mac_text)

    continue_or_exit()

    print_header("Data Structures")

    # Data Structures
    # - Lists
    # - Dictionaries
    # - Tuples
    # - Sets

    print_header("Lists", delimeter="-")
    ic.configureOutput(prefix=prefix("Lists"), includeContext=True)

    list_of_vars = []
    list_of_files = list()
    ic(type(list_of_vars))
    ic(type(list_of_files))

    continue_or_exit()

    file_counter = 0
    ic(file_counter)
    ic(cfg_filename1)
    for letter in cfg_filename1:
        file_counter += 1
        ic(file_counter),
    print(f"\nfile_counter variable is of type {type(file_counter)} and has value {file_counter}")

    continue_or_exit()
    # Create a list
    print(f"Appending cfg_filename1 and cfg_filename2 to list_of_files...")
    list_of_files.append(cfg_filename1)
    list_of_files.append(cfg_filename2)

    # ['retail-rtr.txt', 'csr1000v-1.txt']
    ic(list_of_files)
    ic(len(list_of_files))
    ic(type(list_of_files))

    continue_or_exit()

    print('Lets take the string mac_text and turn it into a list...')
    mac_list = mac_text.split()

    ic(mac_list)
    ic(len(mac_list))

    continue_or_exit()

    print_header("Dictionaries", delimeter="-")
    ic.configureOutput(prefix=prefix("Dictionaries"), includeContext=True)
    # Dictionary Unordered Key:Value pairs
    dict_of_files_brackets = {}
    dict_of_files = dict()

    ic(dict_of_files_brackets)
    ic(type(dict_of_files_brackets))

    ic(dict_of_files)
    ic(type(dict_of_files))

    continue_or_exit()

    print_header("Tuples", delimeter="-")
    ic.configureOutput(prefix=prefix("Tuples"), includeContext=True)


    continue_or_exit()

    print_header("Sets", delimeter="-")
    ic.configureOutput(prefix=prefix("Sets"), includeContext=True)

    mac_set = set(mac_list)

    ic(mac_set)
    ic(type(mac_set))
    ic(len(mac_set))
    ic(len(mac_list))

    continue_or_exit()

    # Input/Output

    # Input
    print_header("Input/Output")
    print_header("Input", delimeter="-")
    ic.configureOutput(prefix=prefix("Input"), includeContext=True)

    continue_or_exit()

    # Output
    print_header("Output", delimeter="-")
    ic.configureOutput(prefix=prefix("Output"), includeContext=True)


    continue_or_exit()


    # Files
    print_header("Files")
    ic.configureOutput(prefix=prefix("Files"), includeContext=True)

    continue_or_exit()

    # Control Structures
    print_header("Control Structures")
    # If/Then
    print_header("if...then", delimeter="-")
    ic.configureOutput(prefix=prefix("if...then"), includeContext=True)

    continue_or_exit()

    # Iteration
    # For Loops
    print_header("for loop", delimeter="-")
    ic.configureOutput(prefix=prefix("for loop"), includeContext=True)

    continue_or_exit()


    # Regular Expressions
    print_header("Pattern Matching")
    ic.configureOutput(prefix=prefix("patterns"), includeContext=True)

    ic("7d00" in mac_text)
    if "7d00" in mac_text:
        print("\nfound 7d00 in text")

    ic("7d00" in mac_list)
    if "7d00" in mac_list:
        print("\nfound 7d00 in list")

    ic("7d00" in mac_set)
    for mac in mac_set:
        if "7d00" in mac:
            print("\nFound mac with 7d00")
            ic(mac)

    continue_or_exit()


    print_header("Python Truth")
    ic.configureOutput(prefix=prefix("PyTruth"), includeContext=True)
    # Python Truth

    ic(bool(files_exist))
    if files_exist:
        print("If file_exists is true print out dict_of_files")
        ic(dict_of_files)

    ic(bool(dict_of_files))
    if dict_of_files:
        print(dict_of_files)
    else:
        print("Dictionary of files is empty and therefore False")

    my_text = ""
    ic(bool(my_text))


if __name__ == "__main__":
   main()