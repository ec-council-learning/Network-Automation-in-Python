import dotenv
import os
import sys
import getpass


# Using builtin sys module for command line arguments
print(f"\n---- Python Builtin sys Module for argv  ----\n")

print(f"Output of sys.argv is of type {type(sys.argv)}:")
print(sys.argv)

exit("\n---- Example of sys.argv")

# Getting input
print(f"\n---- Python Input ----")
username = input("Enter Username: ")
password = input("Enter Password: ")
print(f"\nINPUT: Username {username} with password {password} was entered.\n")


# Getting input without echo on the password
print(f"\n---- Python Input ----")
username = input("Enter Username: ")
password = getpass.getpass("Enter Password: ")

print(f"\nGETPASS: Username {username} with password {password} was entered.\n")
print(f"\nWhy not use getpass.getuser()?  Returns system login: {getpass.getuser()}")


# Load Credentials from environment variables
print("Check Environment Variables BEFORE load_dotenv...")
for evar in os.environ:
    print(f"ENV VAR NAME: {evar}\n\t VALUE: {os.getenv(evar)}")

# The magic happens here..with verbose set to true we will see what is loaded
# from our .env file
dotenv.load_dotenv(verbose=True)

print("\nCheck Environment Variables AFTER load_dotenv...")
for evar in os.environ:
    print(f"NAME: {evar}\n\t VALUE: {os.getenv(evar)}")
evar = 'CODE_RED_PASSWORD'
print(f"\nCheck for Specific Environment Variable {evar}: {os.getenv(evar)}\n")


# Set Environment Variables with os module
evar = 'CODERED_USR'
os.environ['CODERED_USR'] = 'arista'
evar_value = os.getenv(evar)
print(f"\nCheck for Specific Environment Variable {evar}: {evar_value}\n")

print(f"\nOnce the script completes, go into the Python interpreter in your terminal \nand see if the Environment Variables are still in memory!")
