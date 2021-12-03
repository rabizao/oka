![test](https://github.com/rabizao/oka/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/rabizao/oka/branch/main/graph/badge.svg)](https://codecov.io/gh/rabizao/oka)
<a href="https://pypi.org/project/oka">
<img src="https://img.shields.io/pypi/v/oka.svg?label=release&color=blue&style=flat-square" alt="pypi">
</a>
![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue.svg)
[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501845.svg)](https://doi.org/10.5281/zenodo.5501845)
[![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028)
[![User Manual](https://img.shields.io/badge/doc-user%20manual-a0a0a0.svg)](https://rabizao.github.io/oka)
[![API Documentation](https://img.shields.io/badge/doc-API%20%28auto%29-a0a0a0.svg)](https://rabizao.github.io/oka/api)

# oka - Client for OKA repository
[Latest version as a package](https://pypi.org/project/oka)

[Current code](https://github.com/rabizao/oka)

[User manual](https://rabizao.github.io/oka)

[API documentation](https://rabizao.github.io/oka/api)

## Overview
`oka` is a client for Oka repository.
It also provides utilities to process data.

## Installation
### ...as a standalone lib
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI...
pip install --upgrade pip
pip install -U oka
pip install -U oka[full]  # use the flag 'full' for extra functionality (recommended)

# ...or, install from updated source code.
pip install git+https://github.com/rabizao/oka
```
    
### ...from source
```bash
sudo apt install python3.8-venv python3.8-dev python3.8-distutils # For Debian-like systems.
git clone https://github.com/rabizao/oka
cd oka
python3.8 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage






**Hello world**
<details>
<p>

```python3
from oka import Oka, generate_token, toy_df

# Create a pandas dataframe.
df = toy_df()
print(df.head())
"""
   attr1  attr2  class
0    5.1    6.4      0
1    1.1    2.5      1
2    6.1    3.6      0
3    1.1    3.5      1
4    3.1    2.5      0
"""
```

```python3

# Login.
token = generate_token("http://localhost:5000")
client = Oka(token, "http://localhost:5000")

# Store.
id = client.send(df)

# Store again.
id = client.send(df)
"""
Content already stored for id iJ_e4463c51904e9efb800533d25082af2a7bf77
"""

# Fetch.
df = client.get(id)

print(df.head())
"""
   attr1  attr2  class
0    5.1    6.4      0
1    1.1    2.5      1
2    6.1    3.6      0
3    1.1    3.5      1
4    3.1    2.5      0
"""
```

</p>
</details>









**DataFrame by hand**
<details>
<p>

```python3
import pandas as pd
from oka import Oka, generate_token

# Create a pandas dataframe.
df = pd.DataFrame(
    [[1, 2, "+"],
     [3, 4, "-"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2", "class"],
)
print(df.head())
"""
       col 1  col 2 class
row 1      1      2     +
row 2      3      4     -
"""
```

```python3

# Login.
token = generate_token("http://localhost:5000")
client = Oka(token, "http://localhost:5000")

# Store.
id = client.send(df)

# Store again.
id = client.send(df)
"""
Content already stored for id f7_6b9deafec2562edde56bfdc573b336b55cb16
"""

# Fetch.
df = client.get(id)

print(df.head())
"""
       col 1  col 2 class
row 1      1      2     +
row 2      3      4     -
"""
```






**Machine Learning workflow**
<details>
<p>

```python3
import json

from sklearn.ensemble import RandomForestClassifier as RF

from idict import let, idict
from idict.function.classification import fit, predict
from idict.function.evaluation import split
from oka import Oka, generate_token

# Login.
token = generate_token("http://localhost:5000")
cache = Oka(token, "http://localhost:5000")
d = (
        idict.fromtoy()
        >> split
        >> let(fit, algorithm=RF, config={"n_estimators": 55}, Xin="Xtr", yin="ytr")
        >> let(predict, Xin="Xts")
        >> (lambda X: {"X2": X * X, "_history": ...})
        >> [cache]
)
cache.send(d)
print(json.dumps(list(d.history.keys()), indent=2))
"""
ssssssssssssssssssssssssssssssssssssssss
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
----setitem-------------------
444444444444444444444444
3333333333333333333333333
[
  "split----------------------sklearn-1.0.1",
  "fit--------------------------------idict",
  "predict----------------------------idict",
  "RwMG040tZc3XNoJkwkBe6A1aIUGNQ4EAQVqi.uAl"
]
"""
```

```python3
#
# d.show()
```

```python3
#
# print(d.z)
```

```python3
#
# d.show()
```

```python3
#
# # A field '_' means this function is a noop process triggered only once by accessing one of the other provided fields."
# d >>= (lambda _, X2, y: print("Some logging/printing that doesn't affect data...\nX²=\n", X2[:3]))
# d.show()
```

```python3
#
# print("Triggering noop function by accessing 'y'...")
# print("y", d.y[:3])
```

```python3
#
# d.show()
```

```python3
#
# # The same workflow will not be processed again if the same cache is used.
# d = (
#         idict.fromtoy()
#         >> split
#         >> let(fit, algorithm=RF, config={"n_estimators": 55}, Xin="Xtr", yin="ytr")
#         >> let(predict, Xin="Xts")
#         >> (lambda X: {"X2": X * X})
#         >> (lambda _, X2, y: print("Some logging/printing that doesn't affect data...", X2.head()))
#         >> [cache]
# )
# d.show()
```

```python3
#
# cache.send(d)
#
# d = cache.get(d.id)
# d.show()
```


</p>
</details>







## More info
Aside from the papers on [identification](https://arxiv.org/abs/2109.06028)
and on [similarity (not ready yet)](https://), the [PyPI package](https://pypi.org/project/oka) 
and [GitHub repository](https://github.com/davips/rabizao/oka), 
<!-- one can find more information, at a higher level application perspective,  -->
A lower level perspective is provided in the [API documentation](https://rabizao.github.io/oka).



## Grants
This work was supported by Fapesp under supervision of
Prof. André C. P. L. F. de Carvalho at CEPID-CeMEAI (Grants 2013/07375-0 – 2019/01735-0).

.>>>>>>>>> outros <<<<<<<<<<<.
