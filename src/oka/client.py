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
from typing import Union

import jwt
import requests as req
from pandas import DataFrame

from garoupa import ø40, ø, Hosh
from garoupa.misc.colors import id2ansi
from idict import idict
from idict.data.compression import unpack, pack
from idict.persistence.compressedcache import CompressedCache
from oka.config import default_url


def j(r):
    """Helper function needed because flask test_client() provide json as a property(?), not as a method."""
    return r.json() if callable(r.json) else r.json


# TODO (minor): detect identity according to number of digits, to pass it as keyworded argument to idict
# TODO: Replace packing of pandas by json-like or pandas own solution

# TODO: adopt e-mail as a more universal user_id, since they can use other multiuser-capable storages/sites
# TODO: okaserver -> use unique global flask session to avoid complains about sqlite threads
@dataclass
class Oka(CompressedCache):
    """Client for OKA repository

    >>>
    Role:
        - Send/receive datasets or results as pandas DataFrame objects.
        - Send/receive datasets, processed data or results in any format (cannot be visualized on the web).
        - Seamless caching of data within a workflow.

    TODO:
        - Handle posts from command line to spare the user from accessing the web to publish results.
        - Distributed cache (after 'oka.lock(id, state)' is implemented to reserve a job and mark it is still alive).
    """

    # TODO: put sync here also
    token: str = None
    url: str = default_url
    id: str = None
    debug: bool = False

    def __post_init__(self):
        # TODO(minor): verify_signature??
        self.login = jwt.decode(self.token, options={"verify_signature": False})["sub"]
        # TODO: change uid to hybrid? unordered? e o alfabeto?
        # TODO: limitar caracteres do login, pra poder usar b"davips----------------------------"?
        self.user_hosh = ø * (self.login if len(self.login) == 40 else self.login.encode())

    def __contains__(self, item):
        url = f"/api/item/{item}/check"
        return j(self.request(url, "get"))["found"]

    def __setitem__(self, id, value, packing=True):
        if self.debug:
            print("oka:", id2ansi("set"), id)
        content = pack(value, ensure_determinism=False) if packing else value
        if id.startswith("_"):
            url = f"/api/item/{value['_id']}"
            response = self.request(url, "post", data={"create_post": True}, files={"file": content})
        else:
            url = f"/api/item/{id}"
            response = self.request(url, "post", data={"create_post": False}, files={"file": content})
        if not response and self.debug:
            print(f"Content already stored for id {id}")
            return None
        return response

    def __getitem__(self, id, oid="<unknown>", packing=True):
        if self.debug:
            print("oka:", id2ansi("get"), id)
        url = f"/api/item/{id}"
        response = self.request(url, "get")
        if response.status_code == 404:
            return
        if packing:
            return unpack(response.content)
        return response.content

    def __delitem__(self, key):
        pass

    def lockid(self, id):
        pass

    def get(self, id):
        """Get a dataframe, callable or idict from server

        On single-valued idicts, content (dataframe or callable) take precedence over idict and is returned directly."""
        if isinstance(id, Hosh):  # pragma: no cover
            id = id.id
        if not isinstance(id, str):  # pragma: no cover
            raise Exception(f"Wrong id format: {id}; type: {type(id)}")
        value = self.__getitem__(id, oid=id)
        if isinstance(value, DataFrame) or callable(value):
            return value

        # REMINDER: We waste the request above, but return a lazy idict.
        return idict(id, self)

    def send(self, d: Union[DataFrame, idict], name=None, description=None, identity=ø40):
        """Send a dataframe, callable or idict to server"""
        # Create idict.
        if callable(d):
            d = idict(f=d, identity=identity)
        if isinstance(d, DataFrame):
            d = idict(df=d, identity=identity)

        # Build metadata.
        if name:
            d["_name"] = name
        if description:
            d["_description"] = description

        if d.id in self:
            print(f"Content already stored for id {d.id}")
            return d.id

        # Store.
        d >> [[self]]

        return d.id

    def __repr__(self):
        pass

    def __iter__(self):
        pass

    # todo-icones/cores na web
    # todo-checar mem leak
    # todo-client enviar blob
    # todo-enviar DF

    def copy(self):
        raise NotImplementedError

    def request(self, route, method, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "Bearer " + self.token
        r = getattr(req, method)(self.url + route, **kwargs)
        # if not r:  # pragma: no cover
        #     raise Exception(f"[Error] Cannot query server for route {route}. {r.content}")
        if r.status_code == 401:  # pragma: no cover
            raise Exception("Token invalid!")
        return r

    def __lshift__(self, other):
        """Alias to be used within expressions

        `client << value` is equivalent to `client.send(value)` but returns value.

        `value` can be a Data object or a tuple `(value, name, description)`."""
        if isinstance(other, tuple):
            self.send(other[0], *other[1:])
            return self
        self.send(other)
        return self

    def __rmatmul__(self, other):
        """Alias to be used within expressions

        `id@client` is equivalent to `client.get(value)`"""
        return self.get(other)
