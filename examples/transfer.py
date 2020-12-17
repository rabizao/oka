# Transfering data

from oka import oka
from aiuna.step.dataset import dataset

oka.url = "http://localhost:5000"
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

# Methods approach.
from oka.io import send, get
send(data, url="http://localhost:5000")
d = get(did, url="http://localhost:5000")
print(d.uuid)
# ...
