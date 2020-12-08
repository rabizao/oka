import requests

from oka.auth import get_token
from tatu.okast import OkaSt


def get(uuid, url='http://data.analytics.icmc.usp.br'):
    token = get_token(url=url)
    storage = OkaSt(token=token, url=url, close_when_idle=True)
    return storage.fetch(uuid, lazy=False)  # TODO make laziness work


def send(data, url='http://data.analytics.icmc.usp.br'):
    # TODO: how to solve post stored but data failed: check if orphan post exist, and delete it from the begining?
    token = get_token(url=url)
    headers = {'Authorization': 'Bearer ' + token}
    info = {
        "step_ids": [step.id for step in list(data.history)],
        "nattrs": data.X.shape[1],
        "ninsts": data.X.shape[0]
    }
    response = requests.put(url + "/api/posts", headers=headers, json={'data_uuid': data.id, "info": info})
    if response.status_code != 200:
        print(response.json())
        return False

    storage = OkaSt(token=token, url=url, close_when_idle=True)
    storage.store(data)

    response = requests.put(url + "/api/posts/activate", headers=headers, json={'data_uuid': data.id})
    if response.status_code != 200:
        print(response.json())
        return False

    return True
