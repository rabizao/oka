# Get a Dataset

## Function approach

In order to get access to a dataset stored in OKA Repository using the function approach you can do the following:

```python
>>> from oka import Oka, generate_token, new_data
>>> token = generate_token()
>>> client = Oka(token)
>>> # Sending an example data object.
>>> data = new_data(
...     X=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]],
...     y=[0, 0, 1, 1, 0]
... )
>>> client.send(data)
True
>>> # Getting the example data object back.
>>> data = client.get(data.id)
```

Please note that `OID` is the OKA Unique Identifier for datasets and can be found in the dataset description page in the web interface. If you want to know more about the operations that can be done with data objects, please refer to [data operations](../data_operations/index.md) section.
