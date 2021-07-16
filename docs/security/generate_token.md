# Generate Token

In order to get access to resources stored in OKA Repository you will have to first generate your API token. This token does not expire and can be retrieved from:

1. Web interface <a href="https://oka.icmc.usp.br/client" target="_blank">https://oka.icmc.usp.br/client</a>
2. Within Python environment by running:

```Python
from oka import generate_token

token = generate_token()
print(token)
```

By running `generate_token()` you will be prompted to provide your credentials (username and password). Note that this approach is not ideal for unsupervised implementations, since the script will stuck until you provide your credentials.
