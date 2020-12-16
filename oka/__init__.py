#  Copyright (c) 2020. Davi Pereira dos Santos and Rafael Amatte Bisão
#  This file is part of the oka project.
#  Please respect the license. Removing authorship by any means
#  (by code make up or closing the sources) or ignoring property rights
#  is a crime and is unethical regarding the effort and time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
#
#  oka is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  oka is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with oka.  If not, see <http://www.gnu.org/licenses/>.
#

from dataclasses import dataclass

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


@dataclass
class Oka:
    """Handle posts from command line to spare the user from accessing the web to publish results."""
    # TODO: put sync here also
    id: str = None
    url: str = default_url

    def __lshift__(self, other):
        """Can receive a Data object or a tuple (data, name, description)."""
        if isinstance(other, tuple):
            send(other[0], self.url, *other[1:])
        send(other, self.url)

    def __rmatmul__(self, other):
        return get(other, self.url)

    # noinspection PyArgumentList
    def __call__(self, id=None, url=None):
        if url is None:
            url = self.url
        if id is None:
            return self.__class__(url=url)
        return get(id, url)


# For the lazy users, these builtins allow for just calling "import oka" (not great for IDE linters though).
__builtins__.update({
    "Oka": Oka(),
    "get": get,
    "send": send,
})

oka = Oka()
