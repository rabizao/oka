from oka.api import requests, default_url
from oka.client import oka
from oka.auth import get_token
from tatu.okast import OkaSt
from tatu.abs.storage import DuplicateEntryException


def get(uuid, url=default_url):
    # TODO: Acho que faz mais sentido a verificacao seguinte ser feita dentro do OkaSt. Dessa maneira,
    # as funcoes get_token(url), j(r) e requests(method, url, **kwargs) ficariam la e seriam importadas
    # aqui para serem usadas em rotas que nao passam pelo OkaSt, como a de enviar arff direto. Alem disso
    # nao ficariam duplicadas. Atualmente se passar token=None para o OkaSt quebra
    if not oka.token:
        print("Please login before.")
        oka.token = get_token(oka.url)

    storage = OkaSt(token=oka.token, url=url, close_when_idle=True)
    data = storage.fetch(uuid, lazy=False)  # TODO make laziness work
    if not data:
        print(f"[Error] Data with OID {uuid} was not found.")
        return None

    return data


def send(data, url=default_url, name=None, description="No description"):
    if not oka.token:
        print("Please login before.")
        oka.token = get_token(oka.url)
    # TODO: how to solve post stored but data failed: check if orphan post exist, and delete it from the begining?

    # Create inactive Post.
    name = name or "→".join(
        x[:3] for x in data.history ^ "name" if x[:3] not in ["B", "Rev", "In", "Aut", "E"]
    )
    info = {
        "past": list(data.past),
        "nattrs": data.X.shape[1],
        "ninsts": data.X.shape[0]
    }
    # print("hh",data.history)
    dic = {'data_uuid': data.id, "info": info,
           "name": name, "description": description}

    try:
        requests("put", url + "/api/posts", json=dic)
        storage = OkaSt(token=oka.token, url=url, close_when_idle=True)
        storage.store(data, lazy=False)
        # Activate Post.
        requests("put", url + "/api/posts/activate",
                 json={'data_uuid': data.id})
    except DuplicateEntryException as e:
        print(f"[Error] You have already uploaded the dataset with OID {e}.")

    return True
