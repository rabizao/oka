import os
import requests

from getpass import getpass
from dotenv import load_dotenv



def j(r):
    """Helper function needed because flask test_client() provide json as a property(?), not as a method."""
    return r.json() if callable(r.json) else r.json


def intercept_errors(url, **kwargs):
    r = requests.post(url, **kwargs)
    if r.ok:
        return r
    raise Exception(j(r)["errors"]["json"])


def get_token(url):
    load_dotenv('.env')
    token = os.environ.get('TOKEN')
    if not token:
        username = input("Username to connect to OKA: ")
        password = getpass("Password to connect to OKA: ")
        data = {"username": username, "password": password}
        try:
            response = intercept_errors(f"{url}/api/auth/login", json=data)
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
