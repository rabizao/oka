# Intro

OKA Client uses data objects to interact with OKA Repository. Here you will find examples of operations that can be done with data objects.

## Generate a Data Object

### From List

In order to generate a data object from a list you can do the following:

```Python
from oka import new_data

data = new_data(
        X=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        y=[0, 1, 1]
    )

print(data.X)
```

### From ARFF File

To be done

### From Pandas DataFrame

To be done

## Split

To be done
