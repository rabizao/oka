# Client for OKA repository

Install
-------

    sudo apt install python3.8-venv python3.8-dev python3.8-distutils # For Debian-like systems.
    git clone https://github.com/rabizao/oka.git
    cd oka
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -e .

Usage
---

<details>
<summary>Transfering data</summary>
<p>

```python3

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
```

```
Username to connect to OKA: xxxxx
Password: xxxx
00ptEh8jeD4BOtwv0thXenF
```
```python3

# Object "@" approach.
d = did @ oka
print(d.id)
```

```
00ptEh8jeD4BOtwv0thXenF
```
```python3

# Methods approach.
send(data, url="http://localhost:5000")
d = get(did, url="http://localhost:5000")
print(d.uuid)
```

```
oka warning: {'data_uuid': 'Error! Dataset already uploaded'}
00ptEh8jeD4BOtwv0thXenF
```

</p>
</details>