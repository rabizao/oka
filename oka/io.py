import requests

default_url = 'http://data.analytics.icmc.usp.br'


def get(uuid, url=default_url):
    from oka.auth import get_token, j
    token = get_token(url=url)
    if token:
        try:
            from tatu.okast import OkaSt
            storage = OkaSt(token=token, url=url, close_when_idle=True)
            data = storage.fetch(uuid, lazy=False)  # TODO make laziness work
            if data is None:
                raise Exception(f"Data {uuid} not found.")
            return data
        except Exception as e:
            print("oka warning:", str(e))
            return None


def send(data, url=default_url, name=None, description="No description"):
    # TODO: how to solve post stored but data failed: check if orphan post exist, and delete it from the begining?
    from oka.auth import get_token, j

    token = get_token(url=url)
    if token:
        # Create inactive Post.
        name = name or "→".join(x[:3] for x in data.history ^ "name" if x[:3] not in ["B", "Rev", "In", "Aut", "E"])

        headers = {'Authorization': 'Bearer ' + token}
        info = {
            "past": list(data.past.keys()),
            "nattrs": data.X.shape[1],
            "ninsts": data.X.shape[0]
        }
        dic = {'data_uuid': data.id, "info": info, "name": name, "description": description}
        response = requests.put(url + "/api/posts", headers=headers, json=dic)
        if response.status_code != 200:
            print("oka warning:", j(response)["errors"]["json"])
            return False

        try:
            # Insert Data.
            from tatu.okast import OkaSt
            storage = OkaSt(token=token, url=url, close_when_idle=True)
            storage.store(data, lazy=False)

            # Activate Post.
            response = requests.put(url + "/api/posts/activate", headers=headers, json={'data_uuid': data.id})
            if response.status_code != 200:
                print(response.json())
                return False

            return True
        except Exception as e:
            print("oka warning:", str(e))
            return False