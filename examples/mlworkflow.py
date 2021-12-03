# Machine Learning workflow

from sklearn.ensemble import RandomForestClassifier as RF

from idict import let, idict
from idict.function.classification import fit, predict
from idict.function.evaluation import split
from oka import Oka, generate_token
import json

# Login.
token = generate_token()
cache = Oka(token)
d = (
        idict.fromtoy()
        >> split
        >> let(fit, algorithm=RF, config={"n_estimators": 55}, Xin="Xtr", yin="ytr")
        >> let(predict, Xin="Xts")
        >> (lambda X: {"X2": X * X, "_history": ...})
        >> [cache]
)
cache.send(d)
print(json.dumps(list(d.history.keys()), indent=2))
# ...

d.show()
# ...

print(d.z)
# ...

d.show()
# ...

# A field '_' means this function is a noop process triggered only once by accessing one of the other provided fields."
d >>= (lambda _, X2, y: print("Some logging/printing that doesn't affect data...\nX²=\n", X2[:3]))
d.show()
# ...

print("Triggering noop function by accessing 'y'...")
print("y", d.y[:3])
# ...

d.show()
# ...

# The same workflow will not be processed again if the same cache is used.
d = (
        idict.fromtoy()
        >> split
        >> let(fit, algorithm=RF, config={"n_estimators": 55}, Xin="Xtr", yin="ytr")
        >> let(predict, Xin="Xts")
        >> (lambda X: {"X2": X * X})
        >> (lambda _, X2, y: print("Some logging/printing that doesn't affect data...", X2.head()))
        >> [cache]
)
d.show()
# ...

cache.send(d)

d = cache.get(d.id)
d.show()
# ...
