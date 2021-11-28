# DataFrame by hand
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
# ...

# Login.
token = generate_token("http://localhost:5000")
client = Oka(token, "http://localhost:5000")

# Store.
id = client.send(df)

# Store again.
id = client.send(df)
#  ...

# Fetch.
df = client.get(id)

print(df.head())
# ...
