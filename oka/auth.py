import os
from getpass import getpass

from oka.api import requests, j


def get_token(url):
    tries = 0
    ntries = 3

    while tries < ntries:
        tries += 1
        username = input("Username to connect to OKA: ")
        password = getpass("Password to connect to OKA: ")
        data = {"username": username, "password": password}
        response = requests("post", f"{url}/api/auth/login", json=data)
        if response and 'access_token' in j(response):            
            return j(response)['access_token']
        else:
            if tries < ntries:
                print("Authentication error. Please try again.")
    print("Authentication failed.")
    exit()
