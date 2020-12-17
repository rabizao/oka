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

from oka.api import requests, j
from tatu.okast import OkaSt

default_url = 'http://data.analytics.icmc.usp.br'


def get(uuid, url=default_url):
    from oka import oka
    from oka.auth import get_token
    # TODO: Acho que faz mais sentido a verificacao seguinte ser feita dentro do OkaSt. Dessa maneira, 
    # as funcoes get_token(url), j(r) e requests(method, url, **kwargs) ficariam la e seriam importadas 
    # aqui para serem usadas em rotas que nao passam pelo OkaSt, como a de enviar arff direto. Alem disso
    # nao ficariam duplicadas. Atualmente se passar token=None para o OkaSt quebra
    if not oka.token:
        print("Please login before.")
        oka.token = get_token(oka.url)
    storage = OkaSt(token=oka.token, url=url, close_when_idle=True)
    data = storage.fetch(uuid, lazy=False)  # TODO make laziness work
    return data


def send(data, url=default_url, name=None, description="No description"):
    from oka import oka
    from oka.auth import get_token
    from tatu.okast import OkaSt
    if not oka.token:
        print("Please login before.")
        oka.token = get_token(oka.url)
    # TODO: how to solve post stored but data failed: check if orphan post exist, and delete it from the begining?
    
    # Create inactive Post.
    name = name or "→".join(x[:3] for x in data.history ^ "name" if x[:3] not in [
                            "B", "Rev", "In", "Aut", "E"])    
    info = {
        "past": list(data.past.keys()),
        "nattrs": data.X.shape[1],
        "ninsts": data.X.shape[0]
    }
    dic = {'data_uuid': data.id, "info": info,
            "name": name, "description": description}
    response = requests("put", url + "/api/posts", json=dic)    
    storage = OkaSt(token=oka.token, url=url, close_when_idle=True)
    storage.store(data, lazy=False)

    # Activate Post.
    response = requests("put", url + "/api/posts/activate", json={'data_uuid': data.id})
    return True

@dataclass
class Oka:
    """Handle posts from command line to spare the user from accessing the web to publish results."""
    # TODO: put sync here also
    id: str = None
    url: str = default_url
    token: str = None

    def __lshift__(self, other):
        """Can receive a Data object or a tuple (data, name, description)."""
        if isinstance(other, tuple):
            send(other[0], self.url, *other[1:])
        send(other, self.url)

    def __rmatmul__(self, other):
        return get(other, self.url)

    # noinspection PyArgumentList
    def __call__(self, id=None, url=None, token=None):
        if url is None:
            url = self.url
        if token is None:
            token = self.token
        if id is None:
            return self.__class__(url=url)
        return get(id, url, token)


# For the lazy users, these builtins allow for just calling "import oka" (not great for IDE linters though).
__builtins__.update({
    "Oka": Oka(),
    "get": get,
    "send": send,
})

oka = Oka()
