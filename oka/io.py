import os

from tatu.okast import OkaSt

from oka.auth import get_token

def get(uuid, url='http://data.analytics.icmc.usp.br'):
    token = get_token(url=url)
    storage = OkaSt(token=token, url=url)
    return storage.fetch(uuid)
