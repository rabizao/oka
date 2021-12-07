# Hello world
from pandas import DataFrame

from oka import Oka, generate_token, toy_df

# Create a pandas dataframe.
df = toy_df()
df = DataFrame([[1,2,3],[4,5,77]])
# ...

# Login.
token = generate_token()
client = Oka(token)

# Store.
id = client.send(df)
print(id)
#
# # Store again.
# id = client.send(df)
# #  ...
#
# # Fetch.
# df = client.get(id)
#
# print(df.head())
# # ...
