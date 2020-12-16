# Transfering data

# Equivalent forms to use the oka tools:
from oka import *  # ->        implicit (methods or object)
# import oka  #  ->               implicit (methods or object) and shorter, but not good for code linter
# from oka import get, send  #    explicit (methods)
# from oka import oka  #  ->      explicit (object)
# import oka as o  #  ->          explicit namespace for methods or object

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
send(data, url="http://localhost:5000")
d = get(did, url="http://localhost:5000")
print(d.uuid)
# ...
