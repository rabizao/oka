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

import requests as req
from garoupa import ø40
from pandas import DataFrame

from idict import idict
from idict.data.compression import unpack, pack
from idict.persistence.compressedcache import CompressedCache
from oka.config import default_url


def j(r):
    """Helper function needed because flask test_client() provide json as a property(?), not as a method."""
    return r.json() if callable(r.json) else r.json

# TODO (minor): detect identity according to number of digits, to pass it as keyworded argument to idict
# TODO: Replace packing of pandas by json-like or pandas own solution

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

    # Only used in parent class; useless here, but can be used for a Session
    decorator = None

    def __setitem__(self, key, value, packit=True):
        url = f"/api/item/{key}"
        content = pack(value, nondeterministic_fallback=True) if packit else value
        response = j(self.request(url, "post", files={"file": content}))["success"]
        if not response:
            print(f"Content already stored for id {key}")
            return None
        return response

    def __getitem__(self, key, oid="<unknown>"):
        url = f"/api/item/{key}"
        response = self.request(url, "get")
        if not response:
            raise Exception(f"[Error] Missing key {key} for idict with OID {oid}.")
        return unpack(response.content)

    def __delitem__(self, key):
        pass

    def lock(self, id, state):
        pass

    def __contains__(self, item):
        url = f"/api/item/{item}?checkonly=true"
        ret = j(self.request(url, "get"))
        return ret

    def __lshift__(self, other):
        """Can receive a Data object or a tuple (data, name, description)."""
        if isinstance(other, tuple):
            self.send(other[0], *other[1:])
        self.send(other)

    def __rmatmul__(self, other):
        return self.get(other)

    # noinspection PyArgumentList
    def __call__(self, id=None):
        if id is None:
            return self.__class__(url=self.url)
        return self.get(id)

    def request(self, route, method, **kwargs):
        headers = {"Authorization": "Bearer " + self.token}
        r = getattr(req, method)(self.url + route, headers=headers, **kwargs)
        if r.status_code == 401:
            raise Exception("Token invalid!")
        elif r.status_code == 422:
            pass
        else:
            if r.ok:
                return r
            print(r.content)
            print(j(r))
            print(j(r)["errors"])
            msg = j(r)["errors"]["json"]
            print(msg)
            raise Exception(msg)

    def get(self, id):
        """Get a dataframe, callable or idict from server

        On single-valued idicts, content (dataframe or callable) take precedence over idict and is returned directly."""
        value = self.__getitem__(id, oid=id)
        if isinstance(value, DataFrame) or callable(value):
            return value
        dic = {self.__getitem__(v, oid=id) for k, v in value["ids"].items()}
        return idict(dic)
        # if not isinstance(value, dict) or "ids" not in value:
        #     raise Exception("dict containing key 'ids' expected.", type(value), value)

    def send(self, d: Union[DataFrame, idict], name=None, description=None, identity=ø40):
        """Send a dataframe, callable or idict to server"""
        # Create idict.
        if callable(d) or isinstance(d, DataFrame):
            d = idict(df=d, identity=identity)

        # Build metadata.
        if name:
            d["_name"] = name
        if description:
            d["_description"] = description

        # Send descriptor.
        id = "_" + d.id[1:] if len(d.ids) == 1 else d.id
        url = f"/api/item/{id}"
        content = pack({"ids": d.ids})
        metadata = {"id": id, "name": name, "description": description}
        response = j(self.request(url, "post", json=metadata, files={"file": content}))["success"]
        if not response:
            print(f"Content already stored for id {d.id}")
            return d.id

        # Send items. Try to use blob cached in RAM.
        for k, v in d.ids.items():
            if k in d.blobs:
                self.__setitem__(v, d.blobs[k], packit=False)
            else:
                self[v] = d[k]

        # except DuplicateEntryException as e:
        #     if "OKATESTING" not in os.environ:
        #         print(f"[Error] You have already uploaded the dataset with OID {e}.")

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
