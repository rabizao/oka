# Hello world
from oka import Oka, generate_token, toy_df

# Create a pandas dataframe.
df = toy_df()
print(df.head())
# ...

# Login.
token = generate_token()
client = Oka(token)

# Store.
id = client.send(df)

# Store again.
id = client.send(df)
#  ...

# Fetch.
df = client.get(id)

print(df.head())
# ...
