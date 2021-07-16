# Invalidate All Tokens

If for any reason you want to invalidate all your tokens, you can do so by running:

```Python
from oka import Oka
from oka.security import generate_token

token = generate_token()
client = Oka(token)
client.invalidate_all_tokens()
```
