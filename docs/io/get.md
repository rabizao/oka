# Get a Dataset

## Function approach

In order to get access to a dataset stored in OKA Repository using the function approach you can do the following:

```Python
from oka import Oka, generate_token

token = generate_token()
client = Oka(token)
data = client.get("OID")
print(data.X)
```

Please note that `OID` is the OKA Unique Identifier for datasets and can be found in the dataset description page in the web interface. If you want to know more about the operations that can be done with data objects, please refer to [data operations](../data_operations/index.md) section.
