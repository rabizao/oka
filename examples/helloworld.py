# Hello world
from oka import Oka, generate_token, toy_df

# Create a pandas dataframe.
df = toy_df()
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
