import os
import requests

from getpass import getpass
from dotenv import load_dotenv


def get_token(url):
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))
    token = os.environ.get('TOKEN')
    if not token:
        username = input("Username to connect to OKA: ")
        password = getpass("Password to connect to OKA: ")
        data={"username": username, "password": password}
        try:
            response = requests.post(f"{url}/api/auth/login", json=data)
            token = response.json()['access_token']
        except Exception as e:
            print(f"Error: {str(e)}")
            exit()
        f = open(f"{basedir}/.env", "w")    
        f.write(f"TOKEN={token}")
        f.close()
    return token
