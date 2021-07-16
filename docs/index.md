# OKA Client documentation

OKA Client was built in order to provide command-line access to OKA Repository. In order to access OKA Repository platform, please go to <a href="https://oka.icmc.usp.br" target="_blank">https://oka.icmc.usp.br</a>. If you want to host a private version of the repository or access the source code, please go to: <a href="https://github.com/rabizao/oka-repository" target="_blank">https://github.com/rabizao/oka-repository</a>. 
Please note that all URLs provided here refer to the official repository hosted at <a href="https://oka.icmc.usp.br" target="_blank">https://oka.icmc.usp.br</a>. If you are hosting a private version, you will need to change this host to the private host you are using.

---

**Documentation**: <a href="https://rabizao.github.io/oka/" target="_blank">https://rabizao.github.io/oka/</a>

**Source Code**: <a href="https://github.com/rabizao/oka" target="_blank">https://github.com/rabizao/oka</a>

---

## Requirements

Python 3.6+

## Installation

```console
$ pip install oka
```

## Examples

### Get your Token
In order to get access to data stored in OKA Repository you will have to first get your access Token. The Token can be retrieved from:

1. Web interface <a href="https://oka.icmc.usp.br/client" target="_blank">https://oka.icmc.usp.br/client</a>
2. Within Python environment by running:
```Python
from oka import get_token

token = get_token()
print(token)
```
By running the `get_token()` function you will be prompted to provide your credentials (username and password). Note that this approach is not ideal for unsupervised implementations, since the script will stuck until you provide your credentials. If you are running an unsupervised implementation, get your token from the Web interface as described in 1.

### Get a dataset using function approach
In order to get access to a dataset stored in OKA Repository using the function approach you can do the following:

```Python
from oka import Oka, get_token

token = get_token()
client = Oka(token)
client.get("data_uuid")
```

### Send a dataset using function approach
In order to send a data object to OKA Repository using the function approach you can do the following:

```Python
from oka import Oka, get_token, new

d = new(
        X=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        y=[0, 1, 1]
    )

token = get_token()
client = Oka(token)
client.send(data)
```

## License

This project is licensed under the terms of the MIT license.