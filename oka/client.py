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
import os
from dataclasses import dataclass

import numpy
from tatu.abs.storage import DuplicateEntryException
from tatu.okast import OkaSt

from oka.config import default_url


@dataclass
class Oka:
    """Handle posts from command line to spare the user from accessing the web to publish results."""
    # TODO: put sync here also
    token: str = None
    url: str = default_url
    id: str = None

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

    def get(self, uuid):
        okast = OkaSt(token=self.token, url=self.url, close_when_idle=True, threaded=False)
        data = okast.fetch(uuid, lazy=False)  # TODO make laziness work
        if not data:
            raise Exception(f"[Error] Data with OID {uuid} was not found.")
        return data

    def send(self, data, name=None, description="No description"):
        # TODO: how to solve post stored but data failed: check if orphan post exist, and delete it from the begining?
        # Create inactive Post.
        name = name or "→".join(
            x[:3] for x in data.history ^ "name" if x[:3] not in ["B", "Rev", "In", "Aut", "E"]
        )
        info = {
            "nattrs": len(data.X[0]),
            "ninsts": len(data.X),
            "ntargs": len(data.Y[0]) if isinstance(data.Y[0], list) else 1,
            "nclasses": len(set(data.y)) if isinstance(data.Y, numpy.ndarray) else len(set(data.Y)),
            "past": list(data.past)
        }
        dic = {'data_uuid': data.id, "info": info, "name": name, "description": description}

        try:
            okast = OkaSt(token=self.token, url=self.url, close_when_idle=True)
            okast.request("/api/posts", "put", json=dic)
            okast.store(data, lazy=False)
            # Activate Post.
            okast.request("/api/posts/activate", "put", json={'data_uuid': data.id})
        except DuplicateEntryException as e:
            if "OKATESTING" not in os.environ:
                print(f"[Error] You have already uploaded the dataset with OID {e}.")

        return True
