# Send a Dataset

## Function approach

In order to send a dataset to OKA Repository using the function approach you can do the following:

```Python
from oka import Oka, generate_token, new_data

token = generate_token()
client = Oka(token)

data = new_data(
        X=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        y=[0, 1, 1]
    )

result = client.send(data)
print(result.id)
```

If you want to know more about the operations that can be done with data objects, please refer to [data operations](../data_operations/index.md) section.
