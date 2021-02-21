# Transfering data

from oka import oka
from aiuna.step.dataset import dataset
import sys

from tatu.auth import gettoken

oka.url = "http://localhost:5000"
oka.token = gettoken(oka.url, *sys.argv[1:]) if len(sys.argv) > 1 else "no token yet"
data = dataset.data
did = data.id

# Object approach.
oka << data
d = oka(did)
print(d.uuid)
# ...

# Object "@" approach.
d = did @ oka
print(d.id)
# ...

# Function approach.
from oka.io import send, get
send(data, url="http://localhost:5000")
d = get(did, url="http://localhost:5000")
print(d.uuid)
# ...
