from requests import get

loc = get('https://ipapi.co/8.8.8.8/json/')
print (loc.json())


# https://ipapi.co/api/?python#introduction
import ssl
import urllib.request


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://ipapi.co/8.8.8.8/json/"

contents = urllib.request.urlopen(url, context=ctx).read()
print(contents)


Version 0

loc = get('https://ipapi.co/json/')
print (loc.json())



Version 1

import urllib.request
contents = urllib.request.urlopen("https://ipapi.co/8.8.8.8/json/").read()
print(contents)


Version 2
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

contents = urllib.request.urlopen("https://ipapi.co/8.8.8.8/json/", context=ctx).read()
print(contents)


Version 3
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://ipapi.co/8.8.8.8/json/"
contents = urllib.request.urlopen(url, context=ctx).read()
print(contents)

Version 4

import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

ip = "8.8.8.8"

url = f"https://ipapi.co/{ip}/json/"
contents = urllib.request.urlopen(url, context=ctx).read()
print(contents)


Version 5

import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


ip = input("Enter IP to Lookup: ")

url = f"https://ipapi.co/{ip.strip()}/json/"
contents = urllib.request.urlopen(url, context=ctx).read()
print(contents)


Version 6
# Requires installing the requests module

from requests import get

ip = input("Enter IP to Lookup: ")
url = f"https://ipapi.co/{ip.strip()}/json/"

contents = get(url)
print("----- RAW 0utput -----")
print (contents)
print("\n----- FORMATTED Output -----")
print (contents.json())


git diff <filename> 
git log --pretty=oneline
git log --pretty=format:"%h - %an, %ar : %s"

