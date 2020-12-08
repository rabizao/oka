import os
import requests

from getpass import getpass
from dotenv import load_dotenv


def get_token(url):
    load_dotenv('.env')
    token = os.environ.get('TOKEN')
    if not token:
        username = input("Username to connect to OKA: ")
        password = getpass("Password to connect to OKA: ")
        data={"username": username, "password": password}
        try:
            response = requests.post(f"{url}/api/auth/login", json=data)
            if response.status_code == 422:
                print(response.json()['errors'])
                exit()
            token = response.json()['access_token']
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        f = open(".env", "w")    
        f.write(f"TOKEN={token}")
        f.close()
    return token
